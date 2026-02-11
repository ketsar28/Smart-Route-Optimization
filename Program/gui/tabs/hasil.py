from __future__ import annotations

import streamlit as st
import pandas as pd
from typing import Dict, Any, List


def _format_number(value: float) -> str:
    # Format with two decimals and comma as decimal separator
    s = f"{value:,.2f}"
    return s.replace(".", ",")


def _is_academic_mode(result: Dict[str, Any]) -> bool:
    """Cek apakah result berasal dari academic replay."""
    return result.get("mode") == "ACADEMIC_REPLAY"


def _get_iteration_logs(result: Dict[str, Any]):
    """Ambil ACS dan RVND logs dari kedua format pipeline.

    Standard pipeline: result["acs_data"]["iteration_logs"] & result["rvnd_data"]["iteration_logs"]
    Academic replay:   result["iteration_logs"] → filter by phase ACS_SUMMARY / RVND_SUMMARY
    """
    acs_logs = []
    rvnd_logs = []

    if "acs_data" in result and "iteration_logs" in result["acs_data"]:
        # --- Standard pipeline ---
        acs_logs = result["acs_data"]["iteration_logs"]
    elif "iteration_logs" in result:
        # --- Academic replay: ambil summary per cluster ---
        acs_logs = [log for log in result["iteration_logs"]
                    if log.get("phase") == "ACS_SUMMARY"]

    if "rvnd_data" in result and "iteration_logs" in result["rvnd_data"]:
        rvnd_logs = result["rvnd_data"]["iteration_logs"]
    elif "iteration_logs" in result:
        rvnd_logs = [log for log in result["iteration_logs"]
                     if log.get("phase") == "RVND_SUMMARY"]

    return acs_logs, rvnd_logs


def _build_routes_map(result: Dict[str, Any]) -> Dict[int, Dict]:
    """Bangun lookup map cluster_id -> route data dari result.routes[]."""
    routes_map: Dict[int, Dict] = {}
    for route in result.get("routes", []):
        cid = route.get("cluster_id")
        if cid is not None:
            routes_map[cid] = route
    return routes_map


def _display_iteration_logs(result: Dict[str, Any]) -> None:
    """Tampilkan tabel iterasi ACS & RVND sesuai format tesis."""

    acs_logs, rvnd_logs = _get_iteration_logs(result)
    is_academic = _is_academic_mode(result)

    # Lookup map untuk mengisi field yang kosong di summary logs
    routes_map = _build_routes_map(result) if is_academic else {}

    # ── Tabel ACS ──
    if acs_logs:
        st.markdown("### 🐜 Hasil Konstruksi Rute ACS (Ant Colony System)")
        st.markdown("*Solusi awal sebelum optimasi lokal RVND*")

        acs_df_data = []
        for idx, log in enumerate(acs_logs, 1):
            cluster_id = log.get("cluster_id", "")
            distance = log.get('total_distance', 0)
            route_seq = log.get("route_sequence", "-")

            # Ambil data lengkap dari routes map jika ada
            route_data = routes_map.get(cluster_id, {})
            objective = log.get('objective') or route_data.get('objective', 0)

            # Hitung jumlah pelanggan dari urutan rute (exclude depot = 0)
            n_customers = 0
            if route_seq and route_seq != "-":
                nodes = [n.strip() for n in route_seq.replace("-", ",").split(",") if n.strip()]
                n_customers = sum(1 for n in nodes if n != "0")

            row = {
                "Cluster": cluster_id,
                "Kendaraan": log.get("vehicle_type", ""),
                "Rute": route_seq,
                "Jarak (km)": f"{distance:.2f}",
            }

            if is_academic:
                row["Jml Pelanggan"] = n_customers
            else:
                travel_time = log.get('total_travel_time', distance)
                row["Waktu Tempuh"] = f"{travel_time:.2f}"

            row["Fungsi Objektif (Z)"] = f"{objective:.2f}"
            acs_df_data.append(row)

        if acs_df_data:
            df_acs = pd.DataFrame(acs_df_data)
            st.dataframe(df_acs, use_container_width=True, hide_index=True)

        with st.expander("📋 Lihat Detail Rute ACS"):
            for idx, log in enumerate(acs_logs, 1):
                cluster_id = log.get('cluster_id', '?')
                route_seq = log.get('route_sequence', '')
                vehicle = log.get('vehicle_type', '')
                distance = log.get('total_distance', 0)

                route_data = routes_map.get(cluster_id, {})
                objective = log.get('objective') or route_data.get('objective', 0)

                st.markdown(f"**Cluster {cluster_id}** — {vehicle}")
                if route_seq:
                    st.text(f"  Urutan Rute : {route_seq}")
                st.text(f"  Jarak       : {distance:.2f} km")
                st.text(f"  Objektif (Z): {objective:.2f}")

                # Standard pipeline: tampilkan routes_snapshot
                snap = log.get("routes_snapshot", [])
                for ri, route in enumerate(snap):
                    st.text(f"  Snapshot Rute {ri + 1}: {route}")
                st.divider()

    # ── Tabel RVND ──
    if rvnd_logs:
        st.markdown(
            "### 🔄 Hasil Optimasi RVND (Randomized Variable Neighborhood Descent)")
        st.markdown("*Hasil setelah optimasi lokal — solusi akhir*")

        rvnd_df_data = []
        for idx, log in enumerate(rvnd_logs, 1):
            cluster_id = log.get("cluster_id", "")
            distance = log.get('total_distance', 0)
            route_seq = log.get("route_sequence", "-")

            route_data = routes_map.get(cluster_id, {})
            objective = log.get('objective') or route_data.get('objective', 0)

            # Hitung jumlah pelanggan
            n_customers = 0
            if route_seq and route_seq != "-":
                nodes = [n.strip() for n in route_seq.replace("-", ",").split(",") if n.strip()]
                n_customers = sum(1 for n in nodes if n != "0")

            vehicle = log.get("vehicle_type", "") or route_data.get("vehicle_type", "")

            row = {
                "Cluster": cluster_id,
                "Kendaraan": vehicle,
                "Rute": route_seq,
                "Jarak (km)": f"{distance:.2f}",
            }

            if is_academic:
                row["Jml Pelanggan"] = n_customers
            else:
                travel_time = log.get('total_travel_time', distance)
                row["Waktu Tempuh"] = f"{travel_time:.2f}"
                phase_raw = log.get("phase", "RVND")
                row["Fase"] = phase_raw.replace("RVND-", "")

            row["Fungsi Objektif (Z)"] = f"{objective:.2f}"
            rvnd_df_data.append(row)

        if rvnd_df_data:
            df_rvnd = pd.DataFrame(rvnd_df_data)
            st.dataframe(df_rvnd, use_container_width=True, hide_index=True)

        with st.expander("📋 Lihat Detail Rute RVND"):
            for idx, log in enumerate(rvnd_logs, 1):
                cluster_id = log.get('cluster_id', '?')
                route_seq = log.get('route_sequence', '')
                vehicle = log.get('vehicle_type', '')
                distance = log.get('total_distance', 0)

                route_data = routes_map.get(cluster_id, {})
                objective = log.get('objective') or route_data.get('objective', 0)
                if not vehicle:
                    vehicle = route_data.get('vehicle_type', '')

                st.markdown(f"**Cluster {cluster_id}** — {vehicle}")
                if route_seq:
                    st.text(f"  Urutan Rute : {route_seq}")
                st.text(f"  Jarak       : {distance:.2f} km")
                st.text(f"  Objektif (Z): {objective:.2f}")

                snap = log.get("routes_snapshot", [])
                for ri, route in enumerate(snap):
                    st.text(f"  Snapshot Rute {ri + 1}: {route}")
                st.divider()

    if not acs_logs and not rvnd_logs:
        st.info("Belum ada log iterasi. Jalankan optimasi terlebih dahulu.")


def _build_depot_summary_from_result(points: Dict[str, Any], result: Dict[str, Any]) -> Dict[int, Dict]:
    # points: {"depots": [...], "customers": [...]} entries have id,name,x,y
    depots = points.get("depots", [])
    depot_ids = [int(d.get("id", idx)) for idx, d in enumerate(depots)]
    depot_map = {int(d.get("id", i)): d.get("name", "")
                 for i, d in enumerate(depots)}

    per_depot = {did: {"name": depot_map.get(
        did, ""), "distance": 0.0, "customers": []} for did in depot_ids}

    if not result:
        return per_depot

    routes = result.get("routes", [])
    for route in routes:
        # prefer explicit total_distance if present
        dist = float(route.get("total_distance", 0.0) or 0.0)
        seq = route.get("sequence") or []
        stops = route.get("stops") or []
        # determine depot id: try first stop node_id mapping to depot ids, else fallback to first depot
        depot_id = None
        if stops and isinstance(stops, list) and len(stops) > 0:
            first_node = stops[0].get("node_id")
            # If first_node equals 0 and depot ids include 0, use 0; else if first_node matches a depot id, use it
            if first_node in per_depot:
                depot_id = first_node
            else:
                # try to map 0 -> any depot id if only one depot exists
                if len(per_depot) == 1:
                    depot_id = next(iter(per_depot.keys()))
        if depot_id is None:
            depot_id = next(iter(per_depot.keys())) if per_depot else 0

        per_depot.setdefault(depot_id, {"name": depot_map.get(
            depot_id, ""), "distance": 0.0, "customers": []})
        per_depot[depot_id]["distance"] += dist
        # add customers from sequence (exclude zeros)
        for node in seq:
            try:
                nid = int(node)
            except Exception:
                continue
            if nid == 0:
                continue
            per_depot[depot_id]["customers"].append(nid)

    return per_depot


def _render_summary_academic(result: Dict[str, Any]) -> None:
    """Render ringkasan khusus academic replay yang punya data biaya sendiri."""
    costs = result.get("costs", {})
    routes = result.get("routes", [])
    dataset = result.get("dataset", {})
    depot_info = dataset.get("depot", {})
    depot_name = depot_info.get("name", "Depot")

    total_distance = sum(r.get("total_distance", 0) for r in routes)
    total_fixed = costs.get("total_fixed_cost", 0)
    total_variable = costs.get("total_variable_cost", 0)
    total_cost = costs.get("total_cost", 0)

    # Kumpulkan semua customer dari semua rute
    all_customers: List[int] = []
    for route in routes:
        seq = route.get("sequence", [])
        for node in seq:
            if int(node) != 0:
                all_customers.append(int(node))

    cust_str = ", ".join(str(c) for c in all_customers) if all_customers else "-"

    summary_data = [{
        "Depot ID": depot_info.get("id", 0),
        "Nama Depot": depot_name,
        "Total Jarak (km)": f"{total_distance:,.2f}",
        "Biaya Tetap (Rp)": f"{total_fixed:,.0f}",
        "Biaya Variabel (Rp)": f"{total_variable:,.0f}",
        "Total Biaya (Rp)": f"{total_cost:,.0f}",
        "Jumlah Pelanggan": len(all_customers),
        "Daftar Pelanggan": cust_str
    }]

    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    st.info(f"📍 **Total Jarak Keseluruhan:** {_format_number(total_distance)} km")


def _render_summary_standard(result: Dict[str, Any]) -> None:
    """Render ringkasan untuk standard pipeline."""
    points = st.session_state.get("points", {"depots": [], "customers": []})
    per_depot = _build_depot_summary_from_result(points, result)

    summary_data = []
    total_all_distance = 0.0

    user_vehicles = st.session_state.get("user_vehicles", [])
    vehicle_map = {v["id"]: v for v in user_vehicles}

    total_fixed_cost = 0.0
    total_variable_cost = 0.0
    total_all_cost = 0.0

    for idx, (depot_id, info) in enumerate(sorted(per_depot.items(), key=lambda x: int(x[0]))):
        dist = info.get("distance", 0.0) or 0.0
        total_all_distance += float(dist)

        cust_list = info.get("customers", [])
        cust_str = ", ".join(str(c) for c in cust_list) if cust_list else "-"

        # Hitung biaya per depot
        depot_fixed_cost = 0.0
        depot_variable_cost = 0.0

        for route in result.get("routes", []):
            stops = route.get("stops", [])
            if stops and stops[0].get("node_id") == depot_id:
                v_type = route.get("vehicle_type")
                v_dist = route.get("total_distance", 0)
                vehicle = vehicle_map.get(v_type, {})
                depot_fixed_cost += vehicle.get("fixed_cost", 0)
                depot_variable_cost += (v_dist * vehicle.get("variable_cost_per_km", 0))

        total_fixed_cost += depot_fixed_cost
        total_variable_cost += depot_variable_cost
        depot_total_cost = depot_fixed_cost + depot_variable_cost
        total_all_cost += depot_total_cost

        summary_data.append({
            "Depot ID": depot_id,
            "Nama Depot": info.get("name", f"Depot {depot_id}"),
            "Total Jarak (km)": f"{dist:,.2f}",
            "Biaya Tetap (Rp)": f"{depot_fixed_cost:,.0f}",
            "Biaya Variabel (Rp)": f"{depot_variable_cost:,.0f}",
            "Total Biaya (Rp)": f"{depot_total_cost:,.0f}",
            "Jumlah Pelanggan": len(cust_list),
            "Daftar Pelanggan": cust_str
        })

    if summary_data:
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True, hide_index=True)
        st.info(
            f"📍 **Total Jarak Keseluruhan:** {_format_number(total_all_distance)} km")
    else:
        st.warning("Tidak ada data ringkasan depot.")


def render_hasil() -> None:
    st.header("Hasil")

    data_validated = st.session_state.get("data_validated", False)
    result = st.session_state.get(
        "result") or st.session_state.get("last_pipeline_result")

    if not data_validated or not result:
        st.info(
            "Belum ada hasil. Tekan 'Lanjutkan Proses' di tab Input Data atau "
            "jalankan optimasi di tab Proses Optimasi terlebih dahulu.")
        return

    # Tampilkan tabel iterasi
    _display_iteration_logs(result)

    # Ringkasan Solusi Akhir
    st.divider()
    st.subheader("📈 Ringkasan Solusi Akhir")

    if _is_academic_mode(result):
        _render_summary_academic(result)
    else:
        _render_summary_standard(result)

    # Visualisasi
    st.divider()
    try:
        from graph_hasil import render_graph_hasil
        render_graph_hasil()
    except ImportError:
        st.error("Gagal memuat visualisasi rute.")
