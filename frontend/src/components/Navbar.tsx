import { SyntheticEvent, createRef, HTMLInputTypeAttribute } from "react";

interface NavbarProps {
  setTickerSearch: any;
}

export default function Navbar(props: NavbarProps) {
  const setTickerSearch = props.setTickerSearch;

  const input = createRef<HTMLInputElement>();

  function handleSubmit(e: SyntheticEvent) {
    e.preventDefault();
    const ticker = input.current!.value.toUpperCase();
    setTickerSearch(ticker);
  }

  return (
    <div
      id="navbar"
      className="bg-gray-900 px-2 lg:px-4 py-2 lg:py-10 sm:rounded-xl flex justify-between items-center"
    >
      <h1 className="text-2xl lg:text-4xl m-1">StockPad</h1>
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
