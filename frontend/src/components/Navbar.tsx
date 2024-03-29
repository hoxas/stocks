import { SyntheticEvent, createRef } from "react";
import StocksLogo from "../assets/stocks.svg";

interface NavbarProps {
  setTickerSearch: any;
}

export default function Navbar(props: NavbarProps) {
  const setTickerSearch = props.setTickerSearch;

  const input = createRef<HTMLInputElement>();

  function handleSubmit(e: SyntheticEvent) {
    e.preventDefault();
    const ticker = input.current!.value.toUpperCase();
    if (ticker != "") {
      setTickerSearch(ticker);
    }
  }

  return (
    <div
      id="navbar"
      className="bg-gray-900 px-2 lg:px-4 py-2 lg:py-10 sm:rounded-xl flex justify-between items-center"
    >
      <span className="flex items-center">
        <img src={StocksLogo} className="px-1" />
        <h1 className="text-2xl lg:text-4xl m-1 px-1">StockPad</h1>
      </span>
      <form onSubmit={handleSubmit}>
        <div id="input">
          <input
            type="text"
            name="ticker"
            placeholder="Enter ticker symbol (e.g. AAA)"
            className="bg-gray-900 leading-loose"
            ref={input}
          ></input>
          <button type="submit">
            <i className="fa fa-search"></i>
          </button>
        </div>
      </form>
    </div>
  );
}
