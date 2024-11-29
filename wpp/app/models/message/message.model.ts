export interface MessageFragmented {
    id: string;
    content: string;
    from: string;
    to: string;
    timestamp: number;
    phoneNumber: string;
    possibleNames: {
        name?: string;
        shortName?: string;
        pushname?: string;
    };
    response?: string;
    processed_at?: string;
}
