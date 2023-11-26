using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TimeManagementSource
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 3)
            {
                Console.WriteLine("Error");
                return;
            }
            EventList lst = ProjectHandler.CreateList(args[1]);
            List<Session> s = ProjectHandler.CreateSessionList(args[2]);
            Scheduler schedule = new Scheduler(s);
            try
            {

                Console.WriteLine(schedule.ScheduleDay(lst));
            }
            catch (NotEnoughTime e)
            {
                Console.WriteLine("in");
                List<Event> events_not_time = e.ListEvents;
                foreach (Event event_urgent in events_not_time)
                {
                    Console.WriteLine("Warning, not enough time for the following events:");
                    Console.WriteLine(event_urgent);
                }
            }

        }
    }
}
