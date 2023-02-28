import { useEffect, useRef, useState } from "react";
import SelectedStock, { TickerInterface } from "./SelectedStock";
import StockList from "./StockList";

interface MainProps {
  setTickerSearch: any;
  curTicker: any;
}

function parseJSON(str: string | null) {
  if (str != null) {
    return JSON.parse(str);
  }
  return false;
}

export default function Main(props: MainProps) {
  const [stockList, setStockList] = useState(
    parseJSON(localStorage.getItem("stockList")) || []
  );

  useEffect(() => {
    localStorage.setItem("stockList", JSON.stringify(stockList));
  }, [stockList]);

  const [setTickerSearch, curTicker] = [props.setTickerSearch, props.curTicker];
  return (
    <div id="main" className="flex justify-around py-5 pt-8 px-2 sm:px-0">
      <SelectedStock curTicker={curTicker} setStockList={setStockList} />
      <StockList stockList={stockList} setStockList={setStockList} />
    </div>
  );
}
