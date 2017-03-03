export default class Store {

	constructor(name) {
		this.itemList = null;
		this.name = name;
	}

	get items() {
		if(this.itemList == null)
		    this.itemList = JSON.parse(window.localStorage.getItem(this.name) || '[]');
	    return this.itemList;
	}

	set items(items) {
		window.localStorage.setItem(this.name, JSON.stringify(this.itemList = items));
	}

	insert(item) {
		const items = this.items;
		items.push(item);
		this.items = items;
	}
}