import SelectedStock from "./SelectedStock";
import StockList from "./StockList";

interface MainProps {
  setTickerSearch: any;
  curTicker: any;
}

export default function Main(props: MainProps) {
  const [setTickerSearch, curTicker] = [props.setTickerSearch, props.curTicker];
  return (
    <div id="main" className="flex justify-around py-5 pt-8 px-2 sm:px-0">
      <SelectedStock curTicker={curTicker} />
      <StockList />
    </div>
  );
}
