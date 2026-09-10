const API_BASE_URL = 'http://127.0.0.1:8000'

export async function analyzeConfiguration(file) {
  const config = await file.text()

  const response = await fetch(`${API_BASE_URL}/api/analysis`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      config,
      source_file: file.name,
    }),
  })

  if (!response.ok) {
    let message = `Analysis failed (${response.status})`

    try {
      const errorBody = await response.json()
      if (errorBody.detail) {
        message = errorBody.detail
      }
    } catch {
      // Keep the generic error message.
    }

    throw new Error(message)
  }

  return response.json()
}

export async function generateReport(analysis, sourceFile) {
  const response = await fetch(`${API_BASE_URL}/api/reports`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      source_file: sourceFile,
      analysis,
    }),
  })

  if (!response.ok) {
    let message = `Report generation failed (${response.status})`

    try {
      const errorBody = await response.json()
      if (errorBody.detail) {
        message = errorBody.detail
      }
    } catch {
      // Keep the generic error message.
    }

    throw new Error(message)
  }

  const disposition = response.headers.get('content-disposition')
  const filename = disposition?.match(/filename="?([^";]+)"?/)?.[1]

  return {
    blob: await response.blob(),
    filename: filename || 'compliance-report.pdf',
  }
}
