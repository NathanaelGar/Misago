import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { RouteLoader, WindowTitle } from "../../UI"
import { SettingsContext } from "../../Context"
import { HeaderAllThreads } from "./Header"
import { IThreadsProps } from "./Threads.types"
import ThreadsLayout from "./ThreadsLayout"
import ThreadsList from "./ThreadsList"
import { useThreadsQuery } from "./useThreadsQuery"

const ThreadsAll: React.FC<IThreadsProps> = ({ openCategoryPicker }) => {
  const settings = React.useContext(SettingsContext)
  const { data, error, loading } = useThreadsQuery()

  if (!settings) return <RouteLoader />

  const isIndex = settings.forumIndexThreads
  const { threads } = data || { threads: null }

  return (
    <ThreadsLayout openCategoryPicker={openCategoryPicker}>
      <I18n>
        {({ i18n }) => {
          return (
            <>
              <WindowTitle
                index={isIndex}
                title={i18n._(t("threads.title")`Threads`)}
              />
              <HeaderAllThreads settings={settings} />
              <ThreadsList error={error} loading={loading} threads={threads} />
            </>
          )
        }}
      </I18n>
    </ThreadsLayout>
  )
}

export default ThreadsAll