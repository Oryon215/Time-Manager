using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TimeManagementSource
{
    class ProjectHandler
    {
        public static EventList CreateList(string text)
        {
            //convert string to eventlist
            EventList lst_event = new EventList();
            string[] lst = text.Split('$');
            foreach(string s in lst)
            {
                if (s != "")
                {
                    Event e = ProjectHandler.StringToEvent(s);
                    lst_event.Insert(e);
                }
            }
            return lst_event;
        }

        public static List<Session> CreateSessionList(string text)
        {
            //convert string to session list
            List<Session> lst = new List<Session>();
            string[] components = text.Split('\\');
            foreach(string s in components)
            {
                Session session = StringToSession(s);
                lst.Add(session);
            }
            return lst;
        }

        public static Event StringToEvent(string s)
        {
            //convert string to event
            string[] elements = s.Split(' ');
            Type t = (Type)(int.Parse(elements[0]));
            string name = elements[1];
            string description = elements[2];
            Date deadline = Date.ConvertString(elements[3]);
            double time = double.Parse(elements[4]);
            return new Event(t, name, description, deadline, time);
        }
       
        public static Session StringToSession(string s)
        {
            //convert string to session
            string[] elements = s.Split(' ');
            double length = double.Parse(elements[0]);
            double hour = double.Parse(elements[1]);
            return new Session(length, hour);
        }
        
    }
}
