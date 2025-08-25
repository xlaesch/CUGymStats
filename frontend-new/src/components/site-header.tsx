export function SiteHeader({
  showSidebarTrigger: _showSidebarTrigger = true,
}: {
  showSidebarTrigger?: boolean
}) {
  return (
    <header className="flex h-(--header-height) shrink-0 items-center gap-2 border-b transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-(--header-height)">
      <div className="flex w-full items-center gap-1 px-4 lg:gap-2 lg:px-6">
        {/* Sidebar trigger removed as it's not displayed on the current page */}
        <h1 className="text-base font-medium">Live Facility Counts</h1>
      </div>
    </header>
  )
}
