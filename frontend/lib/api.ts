const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface UploadResponse {
  file_id: string;
  filename: string;
  text_preview: string;
  word_count: number;
  message: string;
}

export interface AnalysisResult {
  file_id: string;
  claims: Array<{
    claim: string;
    category: string;
    importance: string;
  }>;
  verification_results: Array<{
    claim: string;
    verification_result: string;
  }>;
  questions: string[];
  summary: {
    total_claims: number;
    verified_claims: number;
    questions_generated: number;
  };
}

export const api = {
  async uploadPitchDeck(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/api/pitch-deck/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to upload pitch deck');
    }

    return response.json();
  },

  async analyzePitchDeck(fileId: string): Promise<AnalysisResult> {
    const response = await fetch(`${API_BASE_URL}/api/pitch-deck/analyze/${fileId}`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error('Failed to analyze pitch deck');
    }

    return response.json();
  },

  async analyzePitchDeckWithAgents(fileId: string): Promise<AnalysisResult> {
    const response = await fetch(`${API_BASE_URL}/api/pitch-deck/analyze-with-agents/${fileId}`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error('Failed to analyze pitch deck with agents');
    }

    return response.json();
  },
};
