export class Report {
    constructor(
        public event_type: string,
        public location: string,
        public description: string,
        public phone?: string,
        public email?: string
    ) {}
}
