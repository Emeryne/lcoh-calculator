"""LCOH calculator: levelized cost of hydrogen for geothermal-powered electrolysis in Kenya."""

#LCOH using real values in Kenyan context
def calculate_lcoh(
    capacity_mw = 10,
    capex_per_kw = 2100, #alkaline installed cost, USD/kW (EH2 whitepaper, 2024)
    electricity_cost = 0.07, #USD/kWh generation-level price, Kenyan geothermal tariff cap ~KES 9 (ThinkGeoEnergy)
    efficiency_kwh_per_kg = 58, #plant-level incl. compression to 30 bar (EH2 whitepaper)
    capacity_factor = 0.90, 
    opex_fraction = 0.026, #fixed O&M as fraction of CAPEX, alkaline (EH2 whitepaper)
    lifetime_years = 20,  
    discount_rate = 0.13, #Kenya hydrogen WACC (GIZ Kenya sector analysis, 2025)
    stack_replacement_year = 10, #alkaline stack life up to 10 years (EH2 whitepaper)
    fraction_cost_of_stack = 0.15 #stack replacement as fraction of CAPEX, alkaline (EH2)
):
    """Levilized cost of hydrogen in (USD/kg) for geothermal-powered alkaline electrolyzer."""
    capacity_in_kw = capacity_mw * 1000
    annual_energy_consumed = capacity_in_kw * 8760 * capacity_factor
    annual_H2_in_kg = annual_energy_consumed/efficiency_kwh_per_kg

    capex = capacity_in_kw * capex_per_kw
    annual_opex = annual_energy_consumed * electricity_cost + capex * opex_fraction 
    replacement_cost = capex * fraction_cost_of_stack

    presentValue = capex
    presentValue_H2_cost = 0

    for years in range(1, lifetime_years + 1):
        discount_factor = 1/(1+discount_rate) ** years
        yearly_cost = annual_opex
        if years == stack_replacement_year:
            yearly_cost += replacement_cost

        presentValue += yearly_cost * discount_factor
        presentValue_H2_cost += annual_H2_in_kg * discount_factor

    return presentValue/presentValue_H2_cost