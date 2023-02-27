import Navbar from "./Navbar";
import Main from "./Main";

export default function Dashboard() {
  return (
    <div
      id="dashboard"
      className="bg-gray-800 flex-1 flex flex-col space-y-5 lg:space-y-0 lg:space-x-10 max-w-6xl sm:p-6 sm:my-2 sm:mx-4 sm:rounded-2xl"
    >
      <Navbar />
      <Main />
    </div>
  );
}
