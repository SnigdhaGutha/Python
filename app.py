
import streamlit as st
import pandas as pd

st.set_page_config(page_title="RoadGuard", layout="wide")

st.title("🚗 RoadGuard")
st.subheader("AI-Based Pothole Detection and Warning System")

st.info("Prototype Dashboard - Sample Data")

# Dashboard summary
col1, col2, col3 = st.columns(3)

col1.metric("Total Reports", 1)
col2.metric("Active Potholes", 1)
col3.metric("Current Route", "R001")

st.divider()

# Vehicle progress
st.subheader("Vehicle Progress")

position = st.slider("Move the vehicle", 0, 100, 40)

st.progress(position / 100)

# Warning system
if position >= 80:
    st.error("Pothole reached!")
elif position >= 60:
    st.warning("WARNING: Pothole Ahead!")
else:
    st.success("Road clear ahead")

st.divider()

# Sample report
st.subheader("Saved Pothole Reports")

data = {
    "Report ID": ["P001"],
    "Route": ["R001"],
    "Status": ["Reported"],
    "Confidence": ["87%"]
}

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

st.caption("Sample data only. Live AI and camera integration will be added later.")



# Pothole Report Form
st.divider()
st.header("📝 Submit a Pothole Report")

if "reports" not in st.session_state:
    st.session_state.reports = df.to_dict("records")

with st.form("pothole_report_form"):
    location = st.text_input("Pothole Location")
    
    severity = st.selectbox(
        "Severity",
        ["Low", "Medium", "High"]
    )
    
    description = st.text_area("Description")
    
    submitted = st.form_submit_button("Submit Report")

    if submitted:
        if location.strip() and description.strip():
            report = {
    "Report ID": report_id,
    "Route": route,
    "Status": "Reported",
    "Confidence": confidence,
    "Severity": severity,
}
            st.session_state.reports.append(report)
            st.success("Pothole report submitted successfully!")
        else:
            st.error("Please enter the location and description.")


st.subheader("All Pothole Reports")

df = pd.DataFrame(st.session_state.reports)
st.dataframe(df, use_container_width=True)

if st.session_state.reports:
    report_ids = [
        report["Report ID"]
        for report in st.session_state.reports
    ]

    selected_id = st.selectbox(
        "Select Report to Delete",
        report_ids
    )

    if st.button("Delete Report"):
        st.session_state.reports = [
            report for report in st.session_state.reports
            if report["Report ID"] != selected_id
        ]
        st.success("Report deleted successfully!")
        st.rerun()


st.subheader("Update Report Status")

if st.session_state.reports:
    report_ids = [
        report["Report ID"]
        for report in st.session_state.reports
    ]

    selected_report = st.selectbox(
        "Select Report",
        report_ids,
        key="update_report"
    )

    new_status = st.selectbox(
        "New Status",
        ["Reported", "In Progress", "Resolved"]
    )

    if st.button("Update Status"):
        for report in st.session_state.reports:
            if report["Report ID"] == selected_report:
                report["Status"] = new_status

        st.success("Report status updated!")
        st.rerun()

st.subheader("Pothole Status Summary")



if st.session_state.reports:
    df_status = pd.DataFrame(st.session_state.reports)

    all_statuses = ["Reported", "In Progress", "Resolved"]
    status_counts = (
        df_status["Status"]
        .value_counts()
        .reindex(all_statuses, fill_value=0)
    )

    st.bar_chart(status_counts)
else:
    st.info("No reports available.")

st.subheader("Pothole Severity Summary")

if st.session_state.reports:
    df_severity = pd.DataFrame(st.session_state.reports)

    if "Severity" in df_severity.columns:
        severity_counts = df_severity["Severity"].value_counts()
        st.bar_chart(severity_counts)
    else:
        st.info("Severity data is missing from reports.")
else:
    st.info("No reports available.")
