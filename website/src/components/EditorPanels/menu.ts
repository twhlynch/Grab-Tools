export type MenuLeaf =
	| {
			func: (e?: Event) => void;
			file?: boolean;
	  }
	| {
			href: string;
	  };

export type MenuItem = MenuLeaf | Menu;

export interface Menu {
	[key: string]: MenuItem;
}
