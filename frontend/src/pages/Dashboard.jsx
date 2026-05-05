const Dashboard = () => {
  // Thay thế đường link này bằng link "Publish to web" thật của bạn từ Power BI
  const powerBiPublicUrl = "https://app.powerbi.com/view?r=eyJrIjoi...YOUR_LINK_HERE...";

  return (
    <div className="dashboard-container" style={{ width: "100%", height: "800px" }}>
      <iframe
        title="Power BI Dashboard"
        width="100%"
        height="100%"
        src={powerBiPublicUrl}
        frameBorder="0"
        allowFullScreen={true}
        style={{ border: "none", borderRadius: "8px", boxShadow: "0 4px 12px rgba(0,0,0,0.1)" }}
      ></iframe>
    </div>
  );
};

export default Dashboard;
