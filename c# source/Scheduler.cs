using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace TimeManagementSource
{
    public class Session
    {
        public double start_hour;
        public double length;

        public Session( double l, double hour)
        {
            this.length = l;
            this.start_hour = hour;
        }
        public override string ToString()
        {
            return "start:" + this.start_hour.ToString() + " " + "length:" + this.length.ToString();
        }
    }
    class Scheduler

    {
        public static double open_hours = 16; // available hours a day for the average man
        public double sum; // total hours available for each instance
        public List<Session> sessions = new List<Session>();

        public Scheduler(List<Session> sessions)
        {
            this.sum = 0;
            foreach (var session in sessions)
            {
                sum += session.length;
            }
            if (sum <= Scheduler.open_hours)
            {
                this.sessions = sessions;
            }
        }

        public Event IsUrgent(List<Event> lst)
        {
            //return an urgent event if a list has one, otherwise return null
            if (lst.Count == 0)
            {
                return null;
            }
            Date deadline = lst[0].Deadline;
            Date current = Date.GetCurrent();
            current.Day += 1;
            if (deadline.CompareTo(current) == 0)
            {
                Event return_Value = lst[0];
                lst.RemoveAt(0);
                return return_Value;
            }
            return null;
        }

        public Event Urgent(EventList lst)
        {
            //return the most urgent event
            foreach(List<Event> event_lst in lst.Events.Values)
            {
                Event e = this.IsUrgent(event_lst);
                if (e != null)
                {
                    return e;
                }
            }
            return null;
        }

        public bool HandleUrgent(Day d, Event e)
        {
            //schedule urgent event
            if (this.sum < e.Time)
            {
                return false;
            }
            double len_break = 0.5;
            int num_sessions = (int)Math.Ceiling(e.Time / 0.75);
            double left_over = e.Time % 0.75;

            if (e.Time + (num_sessions - 1) * len_break > this.sum) // if breaktime is not enough
            {
                len_break = (this.sum - e.Time) / (num_sessions - 1); // change breaktime
            }

            if(e.Time > 0 && sessions.Count > 0) 
            {
                Event left = this.InsertSession(d, e, sessions[0], len_break);
                while (left != null)
                {
                    sessions.RemoveAt(0);
                    left = this.InsertSession(d, left, sessions[0], len_break);
                }
            }
            return true;
        }

        public Event InsertSession(Day d, Event e, Session s, double len_break = 0.5)
        {
            //start with 45 minute intervals
            while (s.length >= 0.75 + len_break && e.Time >= 0.75)
            {

                Event small = new Event(e.Type_Event, e.Name, e.Description, e.Deadline, 0.75);
                d.QueueEvent(small, s.start_hour);
                s.start_hour += 0.75;
                if (len_break > 0)
                {
                    Event break_activity = new Event("break", "Leisure time", len_break);
                    d.QueueEvent(break_activity, s.start_hour);
                    s.start_hour += len_break;
                    s.length -= 0.75 + len_break;
                }
                e.Time -= 0.75;
            }

            //check if finished
            if (e.Time == 0)
            {
                return null;
            }

            //if we can finish task
            if (e.Time < 0.75 && s.length >= e.Time)
            {

                Event small = new Event(e.Type_Event, e.Name, e.Description, e.Deadline, e.Time);
                d.QueueEvent(small, s.start_hour);
                s.start_hour += e.Time;
                s.start_hour += len_break;
                s.length -= e.Time;
                e.Time = 0;
                return null;
            }
            else if (s.length > 0) //otherwise return left over
            {

                Event small = new Event(e.Type_Event, e.Name, e.Description, e.Deadline, s.length);
                d.QueueEvent(small, s.start_hour);
                s.start_hour += s.length;
                e.Time -= s.length;
                s.length = 0;

            }
            Event return_value = new Event(e.Type_Event, e.Name, e.Description, e.Deadline, e.Time);
            return return_value;
        }


        public Day ScheduleDay(EventList lst)
        {
            List<Event> not_enough_time = new List<Event>();
            Day d = new Day();
            //handle_urgents
            Event e = this.Urgent(lst);
            while (e != null)
            {
                if (!this.HandleUrgent(d, e))
                {
                    not_enough_time.Add(e);
                }
                e = this.Urgent(lst);
            }
            if (not_enough_time.Count > 0)
            {
                throw new NotEnoughTime(not_enough_time);
            }


            //handle_regulars
            Type[] types = new Type[] { Type.imp_1_urg_1, Type.imp_1_urg_0, Type.imp_0_urg_1 };
            int index_type = 0;
            while (sessions.Count > 0)
            {
                Event event_regular = lst.Pop(types[index_type % 3]);
                if (event_regular == null)
                {
                    break;
                }
                this.InsertSession(d, event_regular, sessions[0]);
                if (sessions[0].length == 0)
                {
                    sessions.RemoveAt(0);
                }
                index_type++;
            }
            //add breaks
            while (sessions.Count > 0)
            {
                Event random = lst.Pop();
                if (random == null)
                {
                    random = new Event("break", "Leisure time", 0.5);

                }

                if (sessions[0].length == 0)
                {
                    sessions.RemoveAt(0);
                }
                else
                {
                    this.InsertSession(d, random, sessions[0], 0);
                }
            }

            return d;
        }
        
    }
}
