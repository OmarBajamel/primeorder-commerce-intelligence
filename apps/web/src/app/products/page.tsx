import type { Metadata } from "next"; import { DashboardView } from "@/components/dashboard-view";
export const metadata: Metadata = { title: "Products & Categories" }; export default function Page() { return <DashboardView route="products" />; }
