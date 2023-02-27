export default function Navbar() {
  return (
    <div
      id="navbar"
      className="bg-gray-900 px-2 lg:px-4 py-2 lg:py-10 sm:rounded-xl flex justify-between items-center"
    >
      <h1 className="text-2xl lg:text-4xl m-1">StockPad</h1>
      <div id="input">
        <input
          type="text"
          name="ticker"
          placeholder="Enter ticker symbol (e.g. AAA)"
          className="bg-gray-900 leading-loose"
        ></input>
        <button type="submit">
          <i className="fa fa-search"></i>
        </button>
      </div>
    </div>
  );
}
