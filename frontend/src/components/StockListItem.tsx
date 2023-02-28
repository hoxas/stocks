import { TickerInterface } from "./SelectedStock";

interface ListItemProps {
  stock: TickerInterface;
  setTickerSearch: any;
}

export default function ListItem(props: ListItemProps) {
  const [setTickerSearch] = [props.setTickerSearch];

  return (
    <li
      className="p-2 hover:bg-gray-600 flex-grow inline-flex justify-between"
      onClick={() => setTickerSearch(props.stock.ticker)}
    >
      <span>{props.stock.ticker}</span>
      <span className="pr-2">{props.stock.price}</span>
    </li>
  );
}
