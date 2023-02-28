import ListItem from "./StockListItem";

export default function StockList() {
  return (
    <div id="stock-list" className="flex-grow px-5 py-4">
      <div className="flex justify-between items-center">
        <h3>Stock List (StockNumber)</h3>
        <div className="items-center space-x-2">
          <a className="bg-gray-900 text-white/50 p-2 rounded-md hover:text-white smooth-hover">
            <i className="fa fa-refresh"></i>
          </a>
          <a className="bg-gray-900 text-white/50 p-2 rounded-md hover:text-white smooth-hover">
            <i className="fa fa-bookmark"></i>
          </a>
        </div>
      </div>
      <ul className="mt-5 bg-gray-700">
        <ListItem>stock 1</ListItem>
        <ListItem>stock 2</ListItem>
        <ListItem>stock 3</ListItem>
        <ListItem>stock 3</ListItem>
        <ListItem>stock 3</ListItem>
        <ListItem>stock 3</ListItem>
        <ListItem>stock 3</ListItem>
      </ul>
    </div>
  );
}
