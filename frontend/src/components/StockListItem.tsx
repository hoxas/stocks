import { PropsWithChildren } from "react";

export default function ListItem(props: PropsWithChildren) {
  return <li className="p-2 hover:bg-gray-600">{props.children}</li>;
}
