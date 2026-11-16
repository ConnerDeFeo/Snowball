// One transaction row on a Form 4. Numbers can be null when the filing leaves them blank.
export interface InsiderTransaction {
  date: string
  insider: string
  position: string
  code: string
  description: string
  security_type: string
  shares: number | null
  price: number | null
  value: number | null
  remaining: number | null
}

// One insider filing. id is "{filing_date}_{accession}"; form is "4" | "13D".
// transactions is empty for 13D.
export interface InsiderFiling {
  id: string
  form: string
  filing_date: string
  filer: string
  transactions: InsiderTransaction[]
}

export interface InsiderBody {
  markdown: string
}
