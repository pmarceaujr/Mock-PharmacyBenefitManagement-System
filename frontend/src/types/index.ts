export interface Member {
    id: number;
    member_id: string;
    first_name: string;
    last_name: string;
    date_of_birth: string;
    gender: string;
    email: string;
    phone: string;
    address: {
        line1: string;
        line2?: string;
        city: string;
        state: string;
        zip_code: string;
    };
    plan_type: string;
    group_id: string;
    effective_date: string;
    termination_date?: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface Drug {
    id: number;
    ndc: string;
    name: string;
    generic_name?: string;
    brand_name?: string;
    is_generic: boolean;
    therapeutic_class: string;
    drug_class: string;
    strength: string;
    dosage_form: string;
    route: string;
    manufacturer: string;
    awp: number;
    package_size: number;
    is_active: boolean;
}

export interface Pharmacy {
    id: number;
    ncpdp_id: string;
    npi: string;
    name: string;
    chain_name?: string;
    phone: string;
    address: {
        line1: string;
        line2?: string;
        city: string;
        state: string;
        zip_code: string;
    };
    location: {
        latitude: number;
        longitude: number;
    };
    pharmacy_type: string;
    is_24_hours: boolean;
    in_network: boolean;
    network_tier: string;
    is_active: boolean;
}

export interface Claim {
    id: number;
    claim_number: string;
    rx_number: string;
    member_id: number;
    drug_id: number;
    pharmacy_id: number;
    fill_date: string;
    quantity: number;
    days_supply: number;
    refills_authorized: number;
    refill_number: number;
    prescriber: {
        npi: string;
        name: string;
    };
    pricing: {
        submitted_amount: number;
        ingredient_cost: number;
        dispensing_fee: number;
        sales_tax: number;
        plan_paid_amount: number;
        member_copay: number;
        member_coinsurance: number;
        deductible_applied: number;
        total_cost: number;
    };
    status: "pending" | "approved" | "paid" | "denied" | "reversed";
    rejection_code?: string;
    rejection_reason?: string;
    flags: {
        is_generic_substitution: boolean;
        requires_prior_auth: boolean;
        is_compound: boolean;
        is_specialty: boolean;
    };
    submitted_at: string;
    processed_at?: string;
    paid_at?: string;
    member?: Member;
    drug?: Drug;
    pharmacy?: Pharmacy;
}

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    pages: number;
    current_page: number;
}

export interface DashboardStats {
    period_days: number;
    start_date: string;
    summary: {
        total_claims: number;
        total_cost: number;
        average_cost: number;
    };
    generic_vs_brand: Array<{
        type: "Generic" | "Brand";
        claims: number;
        cost: number;
    }>;
    top_drugs: Array<{
        name: string;
        is_generic: boolean;
        claims: number;
        total_cost: number;
    }>;
    status_breakdown: Array<{
        status: string;
        count: number;
    }>;
}

export interface TrendData {
    period_days: number;
    trends: Array<{
        date: string;
        claims: number;
        cost: number;
        moving_avg_claims: number;
        moving_avg_cost: number;
    }>;
}

export interface HighUtilizer {
    member_id: string;
    name: string;
    claim_count: number;
    total_cost: number;
    avg_cost_per_claim: number;
}

export interface GenericSavingsOpportunity {
    brand_name: string;
    generic_name: string;
    brand_claims: number;
    avg_brand_cost: number;
    avg_generic_cost: number;
    potential_savings: number;
    savings_per_claim: number;
}

export interface CostSummaryReport {
    report_period: {
        start_date: string;
        end_date: string;
    };
    overall_summary: {
        total_claims: number;
        total_cost: number;
        plan_paid: number;
        member_paid: number;
        average_cost: number;
    };
    by_status: Array<{
        status: string;
        claims: number;
        cost: number;
    }>;
    monthly_breakdown: Array<{
        year: number;
        month: number;
        claims: number;
        cost: number;
    }>;
}
