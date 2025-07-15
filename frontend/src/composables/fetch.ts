export interface FetchResponse<T> extends Response {
  json(): Promise<T>
}

export async function $fetch<T>(url: string, options?: RequestInit): Promise<FetchResponse<T>> {
  const response = await fetch(url, options)

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(`HTTP error! status: ${response.status}, text: ${errorText}`)
  }

  return response as FetchResponse<T>
}
