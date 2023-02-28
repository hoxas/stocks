import { TickerInterface } from "./SelectedStock";

interface ListItemProps {
  stock: TickerInterface;
}

export default function ListItem(props: ListItemProps) {
  return (
    <li className="p-2 hover:bg-gray-600 inline-flex justify-between">
      <span>{props.stock.ticker}</span>
      <span>{props.stock.price}</span>
    </li>
  );
}
