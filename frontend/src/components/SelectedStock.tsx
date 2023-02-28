interface SelectedStockProps {
  curTicker: TickerInterface;
}

interface TickerInterface {
  ticker: string;
  price: string;
}

export default function SelectedStock(props: SelectedStockProps) {
  const curTicker = props.curTicker;

  return (
    <div
      id="selected-stock"
      className="flex-grow px-5 py-4 bg-gray-900/60 rounded-xl"
    >
      <div className="flex justify-between items-center">
        <h3>Current Stock</h3>
        <div className="items-center space-x-2">
          <a className="bg-gray-900 text-white/50 p-2 rounded-md hover:text-white smooth-hover">
            <i className="fa fa-refresh"></i>
          </a>
          <a className="bg-gray-900 text-white/50 p-2 rounded-md hover:text-white smooth-hover">
            <i className="fa fa-bookmark"></i>
          </a>
        </div>
      </div>
      <div className="flex items-center px-16 pb-5 h-full w-full ">
        <div className="flex-grow text-center text-gray-500 text-3xl">
          {curTicker.ticker}
          <hr className="border-gray-500 my-1.5" />
          {curTicker.price}
        </div>
      </div>
    </div>
  );
}
