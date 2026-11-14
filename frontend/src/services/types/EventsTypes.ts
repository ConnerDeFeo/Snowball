// One 8-K's metadata. id is "{filing_date}_{accession}"; date_of_report (the event date) can be null.
export interface EventMeta {
  id: string
  filing_date: string
  date_of_report: string | null
  items: string[]
}

export interface EventBody {
  markdown: string
}
