// Short labels for the common 8-K item numbers; anything else shows its raw item number.
export const EIGHT_K_ITEMS: Record<string, string> = {
  '1.01': 'Material Agreement',
  '1.02': 'Agreement Terminated',
  '1.05': 'Cybersecurity Incident',
  '2.01': 'Acquisition / Disposition',
  '2.02': 'Earnings Results',
  '2.03': 'New Debt',
  '2.05': 'Restructuring',
  '3.02': 'Unregistered Equity Sale',
  '5.02': 'Officer / Director Change',
  '5.03': 'Charter / Bylaw Change',
  '5.07': 'Shareholder Vote',
  '7.01': 'Reg FD Disclosure',
  '8.01': 'Other Events',
  '9.01': 'Exhibits',
}

// "Item 2.02" -> "Earnings Results"
export function itemLabel(item: string): string {
  const number = item.replace(/^item\s+/i, '')
  return EIGHT_K_ITEMS[number] ?? `Item ${number}`
}
