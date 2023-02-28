import { useEffect, useState } from "react";
import axios from "axios";

import Navbar from "./Navbar";
import Main from "./Main";

export default function Dashboard() {
  const [tickerSearch, setTickerSearch] = useState("");
  const [curTicker, setCurTicker] = useState({
    ticker: "TICKER",
    price: "PRICE",
  });

  useEffect(() => {
    axios
      .get(`http://localhost:5000/api/${tickerSearch}`)
      .then((res) => {
        console.log(res);
        setCurTicker(res.data[0]);
      })
      .catch((err) => console.log(err));
  }, [tickerSearch]);

  return (
    <div
      id="dashboard"
      className="bg-gray-800 flex-1 flex flex-col space-y-5 lg:space-y-0 lg:space-x-10 max-w-6xl sm:p-6 sm:my-2 sm:mx-4 sm:rounded-2xl"
    >
      <Navbar setTickerSearch={setTickerSearch} />
      <Main setTickerSearch={setTickerSearch} curTicker={curTicker} />
    </div>
  );
}
