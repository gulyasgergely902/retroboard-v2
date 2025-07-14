export interface Note {
  id: number
  description: string
  category: number
  tags: string[]
}

export interface Category {
  id: number
  name: string
}

export interface Board {
  id: number
  name: string
}
