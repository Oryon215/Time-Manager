using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TimeManagementSource
{
    public enum Type
    {
        //event types
        imp_0_urg_0,
        imp_1_urg_0,
        imp_0_urg_1,
        imp_1_urg_1,
        
    }

    class TypeExtention
    {
        public static string TypeToString(Type t)
        {
            switch (t)
            {
                case Type.imp_0_urg_0:
                    return "NONE";
                case Type.imp_0_urg_1:
                    return "URGNET";
                case Type.imp_1_urg_0:
                    return "IMPORTANT";
                default:
                    return "IMPORTANT_URGENT";
            }
        }
    }


    class Event
    {
        private Type type = Type.imp_0_urg_0;
        private string name;
        private string description;
        private Date deadline = Date.GetCurrent();
        private double time;

        public Event(Type type, string name, string description, Date deadline, double time)
        {
            this.type = type;
            this.name = name;
            this.deadline = deadline;
            this.description = description;
            this.time = time;
        }

        public Event(string name, string description, double time)
        {
            this.name = name;
            this.description = description;
            this.time = time;
        }

        public string Name
        {
            set { this.name = value; }
            get { return this.name; }
        }

        public string Description
        {
            set { this.description = value; }
            get { return this.description; }
        }

        public Date Deadline
        {
            set{ this.deadline = value; }
            get { return this.deadline; }

        }

        public Type Type_Event
        {
            set { this.type = type; }
            get{ return this.type; }
        }

        public double Time
        {
            set { this.time = value; }
            get { return this.time; }
        }

        public override string ToString()
        {

            return name + "," + "Type:" + TypeExtention.TypeToString(type) + ",Deadline:" + deadline.ToString() + "," + description + "," + time * 60 ;
        }
    }
}
