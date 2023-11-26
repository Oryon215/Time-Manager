using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TimeManagementSource
{
    class Date: IComparable
    {
        private static Date current = new Date(DateTime.Now);

        public static Date GetCurrent()
        {
            return current;
        }
        
        public static void SetCurrent(Date d)
        {
            current = new Date(d.day, d.month, d.year);
        }

        public static Date ConvertString(string s)
        {
            // does not handle edge cases
            string[] elements = s.Split('\\');
            int day = int.Parse(elements[0]);
            int month = int.Parse(elements[1]);
            int year = int.Parse(elements[2]);
            return new Date(day, month, year);
        }

        private int day;
        private int month;
        private int year;

        public Date(int day, int month, int year)
        {
            this.day = day;
            this.month = month;
            this.year = year;
        }

        public Date(DateTime d)
        {
            this.day = d.Day;
            this.month = d.Month;
            this.year = d.Year;
        }

        public int Day
        {
            get { return this.day; }
            set { this.day = value; }
        }

        public int Month
        {
            get { return this.month; }
            set { this.month = value; }
        }

        public int Year
        {
            get { return this.year; }
            set { this.year = value; }
        }

        public int CompareTo(object obj)
        {
            if (obj == null) return 1;

            Date other = obj as Date;
            int year = this.year.CompareTo(other.year);
            int month = this.month.CompareTo(other.month);
            int day = this.day.CompareTo(other.day);

            if (year > 0)
            {
                return 1;
            }
            if (year == 0)
            {
                if (month > 0)
                    return 1;

                if (month == 0)
                {
                    if (day > 0)
                    {
                        return 1;
                    }
                    if (day == 0)
                    {
                        return 0;
                    }
                }
            }
            return -1;
        }

        public override string ToString()
        {
            return this.day.ToString() + "/" + this.month.ToString() + "/" + this.year.ToString();  
        }

    }
}
