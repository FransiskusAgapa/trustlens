// shared time range filter utility
// used by ReviewFeed and InsightsPanel to ensure consistent filtering
export const MONTHS = {
    '6months': 6,
    '1year': 12,
    '3years': 36
}

export function filterByTimeRange(items, timeRange, dateField) {
    if (timeRange === 'all') return items
    
    const months = MONTHS[timeRange]
    if (!months) return items

    const cutoff = new Date()
    cutoff.setMonth(cutoff.getMonth() - months)
    
    return items.filter(item => new Date(item[dateField]) >= cutoff)
}