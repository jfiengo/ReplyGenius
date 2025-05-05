import { Link } from 'react-router-dom';
import {
  ChatBubbleLeftRightIcon,
  DocumentTextIcon,
  UserGroupIcon,
  ClockIcon,
  ArrowTrendingUpIcon,
  ArrowPathIcon,
} from '@heroicons/react/24/outline';

const stats = [
  { name: 'Total Conversations', value: '24', icon: ChatBubbleLeftRightIcon, change: '+12%', changeType: 'increase' },
  { name: 'Context Items', value: '156', icon: DocumentTextIcon, change: '+8%', changeType: 'increase' },
  { name: 'Active Customers', value: '89', icon: UserGroupIcon, change: '+4%', changeType: 'increase' },
  { name: 'Avg Response Time', value: '2.4m', icon: ClockIcon, change: '-12%', changeType: 'decrease' },
];

const recentActivity = [
  {
    id: 1,
    type: 'message',
    content: 'New message from John Doe about appointment scheduling',
    time: '2 minutes ago',
  },
  {
    id: 2,
    type: 'context',
    content: 'New context item uploaded: "Service Pricing Guide"',
    time: '15 minutes ago',
  },
  {
    id: 3,
    type: 'message',
    content: 'Conversation with Sarah Smith marked as resolved',
    time: '1 hour ago',
  },
];

const quickActions = [
  {
    name: 'View Messages',
    description: 'Check and respond to customer messages',
    icon: ChatBubbleLeftRightIcon,
    href: '/messages',
  },
  {
    name: 'Upload Context',
    description: 'Add new business context for AI responses',
    icon: DocumentTextIcon,
    href: '/context',
  },
  {
    name: 'View Analytics',
    description: 'Check response times and customer engagement',
    icon: ArrowTrendingUpIcon,
    href: '/analytics',
  },
];

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-10 px-4 sm:px-8">
      <div className="max-w-6xl mx-auto space-y-10">
        {/* Welcome section */}
        <div className="text-center">
          <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 dark:text-white drop-shadow-md">Welcome back! 👋</h2>
          <p className="mt-2 text-lg text-gray-600 dark:text-gray-300">Here's what's happening with your business today.</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => (
            <div
              key={stat.name}
              className="relative overflow-hidden rounded-2xl bg-white dark:bg-gray-800 px-6 pb-8 pt-6 shadow-lg border border-gray-100 dark:border-gray-700 hover:scale-[1.03] transition-transform"
            >
              <dt>
                <div className="absolute -top-4 left-6 rounded-xl bg-primary-500 p-3 shadow-lg">
                  <stat.icon className="h-7 w-7 text-white" aria-hidden="true" />
                </div>
                <p className="ml-16 mt-2 truncate text-base font-medium text-gray-500 dark:text-gray-300">{stat.name}</p>
              </dt>
              <dd className="ml-16 flex items-baseline pb-6 sm:pb-7">
                <p className="text-3xl font-bold text-gray-900 dark:text-white">{stat.value}</p>
                <p
                  className={`ml-2 flex items-baseline text-sm font-semibold ${
                    stat.changeType === 'increase' ? 'text-green-600' : 'text-red-500'
                  }`}
                >
                  {stat.change}
                </p>
              </dd>
            </div>
          ))}
        </div>

        {/* Quick Actions */}
        <div>
          <h3 className="text-lg font-semibold leading-6 text-gray-900 dark:text-white mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {quickActions.map((action) => (
              <Link
                key={action.name}
                to={action.href}
                className="relative flex items-center space-x-4 rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-6 py-6 shadow-md hover:shadow-xl hover:border-primary-400 dark:hover:border-primary-500 transition group"
              >
                <div className="flex-shrink-0 bg-primary-100 dark:bg-primary-900 rounded-full p-3 group-hover:bg-primary-500 group-hover:text-white transition">
                  <action.icon className="h-7 w-7 text-primary-600 group-hover:text-white" aria-hidden="true" />
                </div>
                <div className="min-w-0 flex-1">
                  <span className="absolute inset-0" aria-hidden="true" />
                  <p className="text-lg font-semibold text-gray-900 dark:text-white">{action.name}</p>
                  <p className="truncate text-sm text-gray-500 dark:text-gray-300">{action.description}</p>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-lg font-semibold leading-6 text-gray-900 dark:text-white">Recent Activity</h3>
            <button
              type="button"
              className="inline-flex items-center rounded-md bg-white dark:bg-gray-700 px-3 py-2 text-sm font-semibold text-gray-900 dark:text-white shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600"
            >
              <ArrowPathIcon className="-ml-0.5 mr-1.5 h-5 w-5 text-gray-400 dark:text-gray-300" aria-hidden="true" />
              Refresh
            </button>
          </div>
          <div className="mt-4 flow-root">
            <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
              <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-2xl bg-white dark:bg-gray-800">
                  <ul role="list" className="divide-y divide-gray-200 dark:divide-gray-700">
                    {recentActivity.map((activity) => (
                      <li key={activity.id} className="px-4 py-4 sm:px-6">
                        <div className="flex items-center justify-between">
                          <p className="truncate text-base font-medium text-primary-600 dark:text-primary-400">{activity.content}</p>
                          <div className="ml-2 flex flex-shrink-0">
                            <p className="inline-flex rounded-full bg-green-100 dark:bg-green-900 px-2 text-xs font-semibold leading-5 text-green-800 dark:text-green-200">
                              {activity.time}
                            </p>
                          </div>
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 