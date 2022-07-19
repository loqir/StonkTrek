import React from "react";
import Create from "../components/Create";

export const Banner = () => {
  return <div>Some banner stuff</div>;
};

const Home = () => {
  return (
    <div>
      <h1>Home</h1>
      <div>Have some content</div>
      <Create />
    </div>
  );
};

export default Home;
