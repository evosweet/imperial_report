export class Report {
    constructor(
        public event_type: string,
        public event_id: number,
        public location: string,
        public description: string,
        public phone?: string,
        public email?: string,
        public reportDate?: string,
        public status_id?: string
    ) {}
}
