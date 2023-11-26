using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TimeManagementSource
{
    class EventList
    {
        private Dictionary<Type, List<Event>> events = new Dictionary<Type, List<Event>>() { { Type.imp_1_urg_1, new List<Event>()}, { Type.imp_0_urg_1, new List<Event>() },
            { Type.imp_1_urg_0, new List<Event>() }, {Type.imp_0_urg_0, new List<Event>() } };

        

        public EventList()
        { }


        public Dictionary<Type, List<Event>> Events
        {
            get { return this.events; }
            set { this.events = value; }
        }

        public void InsertToList(Event e, List<Event> lst)
        {
            // insert event to appropriate list in a rising order according to date
            for (int i = 0; i < lst.Count; i++)
            {
                if (e.Deadline.CompareTo(lst[i].Deadline) == 1)
                {
                    lst.Insert(i, e);
                    return;
                }
            }
            lst.Add(e);
        }

        public void Insert(Event e)
        {
            // insert event to eventlist
            this.InsertToList(e, events[e.Type_Event]);
        }

        public Event Pop(Type t, double time = int.MaxValue)
        {
            // return event whose time is less the time variable
            List<Event> list = events[t].Where((e) => e.Time <= time).ToList();
            if (list.Count > 0)
            {
                Event e = list[0];
                events[t].Remove(e);
                return e;

            }
            return null;
        }

        public Event Pop(double time = int.MaxValue)
        {
            // return the first event available
            foreach (Type t in events.Keys)
            {
                
                if (events[t].Count > 0)
                {
                    var return_value =  Pop(t, time);
                    if (return_value != null)
                    {
                        return return_value;
                    }
                }
            }
            return null;
        }

        public override string ToString()
        {
            string s = "";
            foreach(KeyValuePair<Type, List<Event>> pair in this.events)
            {
                s += TypeExtention.TypeToString(pair.Key) + ":\n";
                foreach(Event e in pair.Value)
                {
                    s += e.ToString() + "\n";
                }
            }
            return s;
        }

        
    }
}
