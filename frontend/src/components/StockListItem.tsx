import { TickerInterface } from "./SelectedStock";

interface ListItemProps {
  stock: TickerInterface;
  setTickerSearch: any;
  stockList: TickerInterface[];
  setStockList: any;
}

export default function ListItem(props: ListItemProps) {
  const [stock, setTickerSearch, stockList, setStockList] = [
    props.stock,
    props.setTickerSearch,
    props.stockList,
    props.setStockList,
  ];

  function removeStock(targetStock: TickerInterface) {
    setStockList(
      stockList.filter((stock) => stock.ticker != targetStock.ticker)
    );
  }

  return (
    <li
      className="group p-2 hover:bg-gray-600 flex-grow inline-flex justify-between"
      onClick={() => setTickerSearch(stock.ticker)}
    >
      <span>{stock.ticker}</span>
      <span className="pr-2">
        <span className="px-2">{stock.price}</span>
        <a
          className="px-3 h-full hidden group-hover:inline"
          onClick={() => removeStock(stock)}
        >
          <i className="fa fa-trash text-red-500"></i>
        </a>
      </span>
    </li>
  );
}
