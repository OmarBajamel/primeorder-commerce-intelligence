import type { Metadata } from "next"; import { DashboardView } from "@/components/dashboard-view";
export const metadata: Metadata = { title: "Acquisition & Campaigns" }; export default function Page() { return <DashboardView route="acquisition" />; }
