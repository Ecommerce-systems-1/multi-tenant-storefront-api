"use client";
import { useState, useEffect } from "react";
import TenantTabs from "@/components/TenantTabs";
import StorefrontHeader from "@/components/StorefrontHeader";
import ProductGrid from "@/components/ProductGrid";
import AdminPanel from "@/components/AdminPanel";
import { getConfig, getProducts } from "@/lib/api";

const TENANTS = ["styleseek", "urbankicks", "luxehome"];

export default function Home() {
  const [tenant, setTenant] = useState("styleseek");
  const [config, setConfig] = useState<any>(null);
  const [products, setProducts] = useState<any>(null);
  const [showAdmin, setShowAdmin] = useState(false);

  useEffect(() => {
    Promise.all([getConfig(tenant), getProducts(tenant)])
      .then(([cfg, prods]) => { setConfig(cfg); setProducts(prods); });
  }, [tenant]);

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <TenantTabs tenants={TENANTS} active={tenant} onChange={setTenant} />
      {config && <StorefrontHeader config={config} onAdminToggle={() => setShowAdmin(v => !v)} />}
      {showAdmin && <AdminPanel tenant={tenant} primaryColor={config?.primary_color} onCreated={() => getProducts(tenant).then(setProducts)} />}
      <ProductGrid products={products?.products ?? []} primaryColor={config?.primary_color ?? "#6366f1"} />
    </div>
  );
}