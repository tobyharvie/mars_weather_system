import '../style/About.css'; 

export default function Home() {
  return (
    <div className="about-container">
      <h1 className="text-3xl font-bold">About</h1>
      <p>This data comes from the NASA Insight rover, which landed on the surface of Mars in December 2018</p>
      <h6>A sol is a Martian equivalent to an Earth day. They are measured in days since Insight's landing</h6>
    </div>
  );
}