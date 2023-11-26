using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TimeManagementSource
{
    class HourExtention
    {
        public static string HourToString(double time)
        {
            string hour = ((int)(time / 1)).ToString();
            string minute = ((int)((time % 1) * 60)).ToString();
            if (hour.Length < 2)
            {
                hour = "0" + hour;
            }
            if (minute.Length < 2)
            {
                minute = "0" + minute;
            }
            
return hour + ":" + minute;
        }
    }

    class Day
    {
        private Date d = Date.GetCurrent();
        private List<KeyValuePair<double, Event>> events = new List<KeyValuePair<double, Event>>();
        public int hours_total = 0;

        public Day()
        {

        }

        public Day(Date d)
        {
            this.d = d;
        }

        public void QueueEvent(Event e, double hour)
        {
            if (events.Count == 0)
            for (int i = 0; i < this.events.Count; i++)
            {
                if (hour < events[i].Key && hour > events[i].Key + events[i].Value.Time)
                {
                    events.Insert(i, new KeyValuePair<double, Event>(hour, e));
                        return;
                }
            }
            events.Add(new KeyValuePair<double, Event>(hour, e));
        }

        public override string ToString()
        {
            string s = "";
            foreach(KeyValuePair<double ,Event> pair in events)
            {
                s += HourExtention.HourToString(pair.Key) + ":";
                s += pair.Value.ToString() + "\n" ;
            }
            return s;
        }


    }
}
