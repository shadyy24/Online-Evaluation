-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 18, 2025 at 07:50 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `assessment_tool`
--

-- --------------------------------------------------------

--
-- Table structure for table `ap_category`
--

CREATE TABLE `ap_category` (
  `id` int(11) NOT NULL,
  `category` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ap_category`
--

INSERT INTO `ap_category` (`id`, `category`) VALUES
(1, 'MCA'),
(2, 'BCA');

-- --------------------------------------------------------

--
-- Table structure for table `ap_exam`
--

CREATE TABLE `ap_exam` (
  `id` int(11) NOT NULL,
  `sid` int(11) NOT NULL,
  `num_question` int(11) NOT NULL,
  `mark` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ap_exam`
--

INSERT INTO `ap_exam` (`id`, `sid`, `num_question`, `mark`) VALUES
(1, 1, 5, 1);

-- --------------------------------------------------------

--
-- Table structure for table `ap_exam1`
--

CREATE TABLE `ap_exam1` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `eid` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  `attend` int(11) NOT NULL,
  `correct` int(11) NOT NULL,
  `mark` int(11) NOT NULL,
  `percent` double NOT NULL,
  `status` int(11) NOT NULL,
  `qid` int(11) NOT NULL,
  `sid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ap_exam1`
--

INSERT INTO `ap_exam1` (`id`, `uname`, `eid`, `total`, `attend`, `correct`, `mark`, `percent`, `status`, `qid`, `sid`) VALUES
(1, '101', 1, 5, 5, 2, 1, 20, 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `ap_exam_attend`
--

CREATE TABLE `ap_exam_attend` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `eid` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  `attend` int(11) NOT NULL,
  `correct` int(11) NOT NULL,
  `mark` int(11) NOT NULL,
  `percent` double NOT NULL,
  `status` int(11) NOT NULL,
  `qid` int(11) NOT NULL,
  `sid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ap_exam_attend`
--

INSERT INTO `ap_exam_attend` (`id`, `uname`, `eid`, `total`, `attend`, `correct`, `mark`, `percent`, `status`, `qid`, `sid`) VALUES
(2, '102', 1, 5, 5, 3, 3, 60, 1, 3, 1),
(3, '104', 1, 5, 5, 0, 0, 0, 1, 2, 1),
(4, '105', 1, 5, 5, 2, 2, 40, 1, 7, 1),
(5, '101', 1, 5, 5, 1, 1, 20, 1, 5, 1);

-- --------------------------------------------------------

--
-- Table structure for table `ap_feedback`
--

CREATE TABLE `ap_feedback` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `feedback` varchar(200) NOT NULL,
  `rdate` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ap_feedback`
--

INSERT INTO `ap_feedback` (`id`, `uname`, `feedback`, `rdate`) VALUES
(1, '101', 'require for more training', '14-06-2023');

-- --------------------------------------------------------

--
-- Table structure for table `ap_login`
--

CREATE TABLE `ap_login` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ap_login`
--

INSERT INTO `ap_login` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `ap_staff`
--

CREATE TABLE `ap_staff` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `city` varchar(30) NOT NULL,
  `address` varchar(50) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ap_staff`
--

INSERT INTO `ap_staff` (`id`, `name`, `city`, `address`, `mobile`, `email`, `uname`, `pass`) VALUES
(1, 'Rahul', '', 'Chennai', 8954545121, 'rahul@gmail.com', 'rahul', '123456'),
(2, 'Guru', '', 'Salem', 8856277665, 'guru@gmail.com', 'guru', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `ap_staff_feed`
--

CREATE TABLE `ap_staff_feed` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `regno` varchar(20) NOT NULL,
  `feedback` varchar(100) NOT NULL,
  `rdate` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ap_staff_feed`
--

INSERT INTO `ap_staff_feed` (`id`, `uname`, `regno`, `feedback`, `rdate`) VALUES
(1, 'rahul', '101', 'improve your studies', '20-06-2023');

-- --------------------------------------------------------

--
-- Table structure for table `ap_subcat`
--

CREATE TABLE `ap_subcat` (
  `id` int(11) NOT NULL,
  `cat_id` int(11) NOT NULL,
  `subcat` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ap_subcat`
--

INSERT INTO `ap_subcat` (`id`, `cat_id`, `subcat`) VALUES
(1, 1, 'Java Programming');

-- --------------------------------------------------------

--
-- Table structure for table `ap_temp`
--

CREATE TABLE `ap_temp` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `eid` int(11) NOT NULL,
  `question` varchar(200) NOT NULL,
  `cans` varchar(100) NOT NULL,
  `uans` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ap_temp`
--

INSERT INTO `ap_temp` (`id`, `uname`, `eid`, `question`, `cans`, `uans`) VALUES
(1, '101', 1, 'Which statement is true about a static nested class?', ' It does not have access to nonstatic members of the enclosing class.', ' It does not have access to nonstatic members of the enclosing class.'),
(2, '101', 1, 'Which one of these lists contains only Java programming language keywords?', ' goto, instanceof, native, finally, default, throws', 'class, if, void, long, Int, continue'),
(3, '101', 1, 'What is the Date type of double quoted value?', 'String', 'array'),
(4, '101', 1, 'Which is true about a method-local inner class?', ' It can be marked abstract.', 'It must be marked final.'),
(5, '101', 1, 'Which is a valid keyword in java?', 'interface', 'string');

-- --------------------------------------------------------

--
-- Table structure for table `ap_train_question`
--

CREATE TABLE `ap_train_question` (
  `id` int(11) NOT NULL,
  `cid` int(11) NOT NULL,
  `sid` int(11) NOT NULL,
  `question` varchar(200) NOT NULL,
  `option1` varchar(100) NOT NULL,
  `option2` varchar(100) NOT NULL,
  `option3` varchar(100) NOT NULL,
  `option4` varchar(100) NOT NULL,
  `answer` int(11) NOT NULL,
  `details` text NOT NULL,
  `filename` varchar(50) NOT NULL,
  `qtype` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ap_train_question`
--

INSERT INTO `ap_train_question` (`id`, `cid`, `sid`, `question`, `option1`, `option2`, `option3`, `option4`, `answer`, `details`, `filename`, `qtype`) VALUES
(1, 2, 1, 'Which one of these lists contains only Java programming language keywords?', 'class, if, void, long, Int, continue', ' goto, instanceof, native, finally, default, throws', 'try, virtual, throw, final, volatile, transient', ' strictfp, constant, super, implements, do', 2, 'All the words in option B are among the 49 Java keywords. Although goto reserved as a keyword in Java, goto is not used and has no function.\r\n\r\nOption A is wrong because the keyword for the primitive int starts with a lowercase i.\r\n\r\nOption C is wrong because "virtual" is a keyword in C++, but not Java.\r\n\r\nOption D is wrong because "constant" is not a keyword. Constants in Java are marked static and final.\r\n\r\nOption E is wrong because "include" is a keyword in C, but not in Java.', 'F1dd.txt', 1),
(2, 2, 1, 'Which is a reserved word in the Java programming language?', 'method', 'native', 'subclasses', 'reference', 2, 'The word "native" is a valid keyword, used to modify a method declaration.\r\n\r\nOption A, D and E are not keywords. Option C is wrong because the keyword for subclassing in Java is extends, not ''subclasses''.', '', 1),
(3, 2, 1, 'Which is a valid keyword in java?', 'interface', 'string', 'Float', 'unsigned', 1, 'interface is a valid keyword.\r\n\r\nOption B is wrong because although "String" is a class type in Java, "string" is not a keyword.\r\n\r\nOption C is wrong because "Float" is a class type. The keyword for the Java primitive is float.\r\n\r\nOption D is wrong because "unsigned" is a keyword in C/C++ but not in Java.', '', 1),
(4, 2, 1, 'Which is true about a method-local inner class?', 'It must be marked final.', ' It can be marked abstract.', 'It can be marked public.', ' It can be marked static.', 2, 'Option B is correct because a method-local inner class can be abstract, although it means a subclass of the inner class must be created if the abstract class is to be used (so an abstract method-local inner class is probably not useful).\r\n\r\nOption A is incorrect because a method-local inner class does not have to be declared final (although it is legal to do so).\r\n\r\nC and D are incorrect because a method-local inner class cannot be made public (remember-you cannot mark any local variables as public), or static.', '', 1),
(5, 2, 1, 'Which statement is true about a static nested class?', 'You must have a reference to an instance of the enclosing class in order to instantiate it.', ' It does not have access to nonstatic members of the enclosing class.', ' It''s variables and methods must be static.', 'It must extend the enclosing class.', 2, 'Option B is correct because a static nested class is not tied to an instance of the enclosing class, and thus can''t access the nonstatic members of the class (just as a static method can''t access nonstatic members of a class).', '', 1),
(6, 2, 1, 'Which constructs an anonymous inner class instance?', ' Runnable r = new Runnable() { };', ' Runnable r = new Runnable(public void run() { });', ' Runnable r = new Runnable { public void run(){}};', ' System.out.println(new Runnable() {public void run() { }});', 4, 'D is correct. It defines an anonymous inner class instance, which also means it creates an instance of that new anonymous class at the same time. The anonymous class is an implementer of the Runnable interface, so it must override the run() method of Runnable.', '', 2),
(7, 1, 1, 'What is the Date type of double quoted value?', 'String', 'int', 'array', 'float', 1, '', '', 1);

-- --------------------------------------------------------

--
-- Table structure for table `ap_user`
--

CREATE TABLE `ap_user` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `dob` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `questions` varchar(200) NOT NULL,
  `eid` int(11) NOT NULL,
  `dept` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ap_user`
--

INSERT INTO `ap_user` (`id`, `name`, `gender`, `dob`, `address`, `city`, `mobile`, `email`, `uname`, `pass`, `create_date`, `questions`, `eid`, `dept`) VALUES
(1, 'Pravin', 'Male', '2000-03-23', '56, GD Nagar', 'Karur', 8856545584, 'pravin@gmail.com', '101', '123456', '12-03-2023', '5,1,7,4,3', 1, 'MCA'),
(2, 'Ram', 'Male', '1999-06-05', '44,GG', 'Madurai', 9638527415, 'ram@gmail.com', '102', '1234', '19-04-2023', '3,7,5,1,2', 1, 'MCA'),
(3, 'Siva', 'Male', '1999-06-05', 'Salem', 'Salem', 8856277415, 'siva@gmail.com', '103', '1234', '15-06-2023', '', 0, 'MCA'),
(4, 'Ragu', 'Male', '1998-06-05', 'dd', 'Trichy', 8955744563, 'ragu@gmail.com', '104', '1234', '05-10-2023', '2,3,1,6,7', 1, ''),
(5, 'Jebin', 'Male', '1999-06-05', '54,GG', 'Trichy', 9638527415, 'jebin@gmail.com', '105', '123456', '12-10-2023', '7,1,4,5,3', 1, 'MCA');
