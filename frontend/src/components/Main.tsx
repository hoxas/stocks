import SelectedStock from "./SelectedStock";
import StockList from "./StockList";

export default function Main() {
  return (
    <div id="main" className="flex justify-around py-5 px-2 sm:px-0">
      <SelectedStock />
      <StockList />
    </div>
  );
}
