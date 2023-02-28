import ListItem from "./StockListItem";
import { TickerInterface } from "./SelectedStock";

interface StockListProps {
  stockList: TickerInterface[];
  setStockList: any;
  setTickerSearch: any;
}

export default function StockList(props: StockListProps) {
  const [stockList, setStockList, setTickerSearch] = [
    props.stockList,
    props.setStockList,
    props.setTickerSearch,
  ];

  return (
    <div id="stock-list" className="flex-grow px-5 py-4">
      <div className="flex justify-between items-center">
        <h3>Stock List ({stockList.length})</h3>
        <div className="items-center space-x-2">
          <a className="bg-gray-900 text-white/50 p-2 rounded-md hover:text-white smooth-hover">
            <i className="fa fa-refresh"></i>
          </a>
          <a className="bg-gray-900 text-white/50 p-2 rounded-md hover:text-white smooth-hover">
            <i className="fa fa-bookmark"></i>
          </a>
        </div>
      </div>
      <ul
        className="flex flex-col mt-5 bg-gray-700"
        style={{ maxHeight: "50vh", overflow: "scroll" }}
      >
        {stockList.map((stock, i) => (
          <ListItem key={i} stock={stock} setTickerSearch={setTickerSearch} />
        ))}
      </ul>
    </div>
  );
}
