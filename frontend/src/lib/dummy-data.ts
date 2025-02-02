export const dummyUser = {
  id: "1",
  email: "user@example.com",
  name: "Demo User"
};

export const dummyReports = [
  {
    id: "1",
    created_at: "2024-03-15T10:00:00Z",
    status: "success" as const,
    cse_pdf_url: "https://example.com/cse1.pdf",
    report_url: "https://example.com/report1.pdf",
  },
  {
    id: "2", 
    created_at: "2024-03-14T15:30:00Z",
    status: "pending" as const,
    cse_pdf_url: "https://example.com/cse2.pdf",
    report_url: null,
  },
  {
    id: "3",
    created_at: "2024-03-13T09:15:00Z",
    status: "error" as const,
    cse_pdf_url: "https://example.com/cse3.pdf",
    report_url: null,
  },
];