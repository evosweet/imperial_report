export class MySearch {
    constructor(
        public searchType: string,
        public searchParm: string | number | any,
        public statusId?: number,
        public feedback?: string,
        public id?: number
    ) {}
}
