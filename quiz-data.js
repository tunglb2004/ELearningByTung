window.CourseQuiz = {
  "lessons": [
    {
      "id": "oop1",
      "num": "JC1",
      "module": "Java Core · Phần 1",
      "title": "OOP Principles",
      "javaCore": true
    },
    {
      "id": "java2",
      "num": "JC2",
      "module": "Java Core · Phần 2",
      "title": "Collections",
      "javaCore": true
    },
    {
      "id": "java34",
      "num": "JC3",
      "module": "Java Core · Phần 3–4",
      "title": "Advanced Java",
      "javaCore": true
    },
    {
      "id": "video1",
      "num": "1",
      "module": "PHASE 1",
      "title": "Manual vs Automation"
    },
    {
      "id": "video2",
      "num": "2",
      "module": "PHASE 1",
      "title": "4 Loại Test"
    },
    {
      "id": "phase2",
      "num": "3",
      "module": "PHASE 2",
      "title": "Selenium WebDriver"
    },
    {
      "id": "phase3",
      "num": "4",
      "module": "PHASE 3",
      "title": "TestNG & POM"
    },
    {
      "id": "phase4",
      "num": "5",
      "module": "PHASE 4",
      "title": "Advanced & CI/CD"
    },
    {
      "id": "api1",
      "num": "API1",
      "module": "API Testing · Buổi 1",
      "title": "Fundamentals & HTTP",
      "apiTesting": true
    },
    {
      "id": "api2",
      "num": "API2",
      "module": "API Testing · Tuần 3-4",
      "title": "Auth & Security",
      "apiTesting": true
    },
    {
      "id": "api3",
      "num": "API3",
      "module": "API Testing · RestAssured",
      "title": "RestAssured Automation",
      "apiTesting": true
    }
  ],
  "banks": {
    "oop1": {
      "title": "OOP Principles",
      "questions": [
        {
          "q": "Trong phỏng vấn Java, Encapsulation được hiểu đúng nhất là gì?",
          "options": [
            "Ẩn implementation, chỉ expose hành vi qua public API có kiểm soát",
            "Gom nhiều class vào một package",
            "Kế thừa toàn bộ method từ class cha",
            "Dùng interface thay cho class"
          ],
          "answer": 0,
          "explain": "Encapsulation = data hiding + kiểm soát truy cập qua getter/setter/method, không lộ trực tiếp state."
        },
        {
          "q": "Vì sao balance nên private trong class BankAccount?",
          "options": [
            "Để client không gán balance = -999999, phá business rule",
            "Để compiler chạy nhanh hơn",
            "Vì private là mặc định trong Java",
            "Để không cần viết method"
          ],
          "answer": 0,
          "explain": "Private bảo vệ integrity; thao tác qua deposit/withdraw có validate."
        },
        {
          "q": "Quan hệ 'Dog extends Animal' thể hiện nguyên lý OOP nào?",
          "options": [
            "Inheritance",
            "Encapsulation",
            "Polymorphism",
            "Abstraction"
          ],
          "answer": 0,
          "explain": "extends = kế thừa thuộc tính/hành vi từ class cha."
        },
        {
          "q": "Khi nào KHÔNG nên dùng Inheritance?",
          "options": [
            "Quan hệ là 'has-a' (composition hợp lý hơn)",
            "Cần reuse code",
            "Class con cần override",
            "Cần đa hình"
          ],
          "answer": 0,
          "explain": "Inheritance cho 'is-a'; has-a dùng composition."
        },
        {
          "q": "@Override trong Java báo hiệu điều gì cho compiler?",
          "options": [
            "Method con thay thế implementation method cha",
            "Method mới hoàn toàn",
            "Method static",
            "Method final"
          ],
          "answer": 0,
          "explain": "@Override = override instance method theo contract class cha."
        },
        {
          "q": "Polymorphism runtime (dynamic dispatch) xảy ra khi nào?",
          "options": [
            "Gọi method trên reference cha, object thực tế là con",
            "Khai báo biến kiểu int",
            "Dùng static method",
            "Import package"
          ],
          "answer": 0,
          "explain": "JVM chọn method theo actual object type lúc runtime."
        },
        {
          "q": "Đoạn: Animal a = new Dog(); a.speak(); — speak() gọi bản nào?",
          "options": [
            "Dog.speak() nếu Dog override",
            "Animal.speak() luôn luôn",
            "Không compile",
            "Ngẫu nhiên"
          ],
          "answer": 0,
          "explain": "Dynamic binding: implementation của Dog được gọi."
        },
        {
          "q": "Abstract class khác Interface (Java 8+) ở điểm nào quan trọng?",
          "options": [
            "Abstract class có thể có concrete method + state; interface chủ yếu contract",
            "Interface luôn có constructor",
            "Abstract class không cho phép kế thừa",
            "Không khác nhau"
          ],
          "answer": 0,
          "explain": "Abstract class = partial implementation; interface = capability contract."
        },
        {
          "q": "Abstraction giúp test automation như thế nào?",
          "options": [
            "Test code phụ thuộc interface, đổi implementation (DB, driver) dễ",
            "Không cần locator",
            "Không cần wait",
            "Chỉ chạy manual"
          ],
          "answer": 0,
          "explain": "Abstraction tách contract khỏi implementation — linh hoạt khi đổi MySQL/PostgreSQL driver."
        },
        {
          "q": "protected modifier dùng khi nào?",
          "options": [
            "Subclass/package cần truy cập, nhưng không public ra ngoài",
            "Chỉ trong cùng file",
            "Cho mọi class",
            "Thay cho private"
          ],
          "answer": 0,
          "explain": "protected = visible cho subclass, ẩn với client bên ngoài."
        },
        {
          "q": "Composition over inheritance nghĩa là gì?",
          "options": [
            "Ưu tiên has-a (chứa object) thay vì is-a khi không chắc hierarchy",
            "Không dùng class",
            "Chỉ dùng interface",
            "Viết một class khổng lồ"
          ],
          "answer": 0,
          "explain": "Composition giảm coupling, tránh deep inheritance tree."
        },
        {
          "q": "final class trong Java có ý nghĩa gì?",
          "options": [
            "Không thể bị extend",
            "Không thể instantiate",
            "Không có method",
            "Tự động abstract"
          ],
          "answer": 0,
          "explain": "final class = không cho kế thừa (ví dụ String)."
        },
        {
          "q": "Lỗi thiết kế: public List<Card> cards trong domain model — vấn đề?",
          "options": [
            "Client có thể clear/add trực tiếp, phá encapsulation",
            "List không dùng được",
            "Không serialize được",
            "Không OOP"
          ],
          "answer": 0,
          "explain": "Expose mutable collection public = mất kiểm soát state."
        },
        {
          "q": "Trong interview: '4 trụ cột OOP' — thứ tự trình bày tốt?",
          "options": [
            "Encapsulation → Inheritance → Polymorphism → Abstraction",
            "Chỉ Polymorphism",
            "Ngẫu nhiên",
            "Không có thứ tự"
          ],
          "answer": 0,
          "explain": "Thường bắt từ encapsulation (nền) đến abstraction (thiết kế hệ thống)."
        },
        {
          "q": "Interface với nhiều implementation (MySQL vs Mongo repo) thể hiện?",
          "options": [
            "Polymorphism + Abstraction",
            "Chỉ Encapsulation",
            "Chỉ Inheritance",
            "Không liên quan OOP"
          ],
          "answer": 0,
          "explain": "Repository interface + nhiều impl = đa hình + trừu tượng hóa persistence."
        },
        {
          "q": "Tight coupling là gì và OOP giảm bằng cách nào?",
          "options": [
            "Phụ thuộc chi tiết implementation; giảm bằng abstraction/interface",
            "Viết ít code",
            "Dùng global variable",
            "Không dùng method"
          ],
          "answer": 0,
          "explain": "Loose coupling qua interface/encapsulation dễ test và maintain."
        },
        {
          "q": "Method overloading vs overriding — khác biệt cốt lõi?",
          "options": [
            "Overloading: cùng tên, khác signature, compile-time; Overriding: kế thừa, runtime",
            "Giống nhau",
            "Overloading là runtime",
            "Overriding là compile-time"
          ],
          "answer": 0,
          "explain": "Overload = static binding; Override = dynamic binding."
        },
        {
          "q": "Khi design class User cho automation framework, field password nên?",
          "options": [
            "private, không log, truy cập qua method an toàn",
            "public để test nhanh",
            "static",
            "final và public"
          ],
          "answer": 0,
          "explain": "Bảo mật + encapsulation: không expose credential trong API công khai."
        },
        {
          "q": "LSP (Liskov) liên quan inheritance: class con phải?",
          "options": [
            "Thay thế được class cha mà không phá hành vi mong đợi",
            "Có ít method hơn cha",
            "Không override",
            "Luôn throw Exception"
          ],
          "answer": 0,
          "explain": "LSP: subtype phải usable everywhere supertype dùng được — hay hỏi senior."
        },
        {
          "q": "Tại sao OOP quan trọng với Page Object Model?",
          "options": [
            "POM = đóng gói trang/locator; tái sử dụng & bảo trì theo OOP",
            "POM không dùng class",
            "POM chỉ cho manual test",
            "POM thay Selenium"
          ],
          "answer": 0,
          "explain": "POM áp dụng encapsulation + abstraction cho UI layer."
        }
      ]
    },
    "java2": {
      "title": "Collections",
      "questions": [
        {
          "q": "ArrayList vs LinkedList — khi nào chọn ArrayList cho test data?",
          "options": [
            "Cần truy cập index/random nhanh, ít insert giữa list",
            "Cần insert đầu list liên tục",
            "Cần unique elements",
            "Cần key-value lookup"
          ],
          "answer": 0,
          "explain": "ArrayList O(1) get by index; LinkedList tốt cho insert/delete đầu."
        },
        {
          "q": "HashSet đảm bảo điều gì?",
          "options": [
            "Không duplicate, unordered (mặc định)",
            "Thứ tự insertion",
            "Sorted theo key",
            "Cho phép null nhiều lần"
          ],
          "answer": 0,
          "explain": "Set = unique; HashSet dùng hash table."
        },
        {
          "q": "Map trong automation: lưu locator name → By object phù hợp vì?",
          "options": [
            "Tra cứu O(1) theo key, mô tả rõ ràng",
            "Giữ thứ tự insert",
            "Cho phép duplicate key",
            "Thay cho List"
          ],
          "answer": 0,
          "explain": "Map = key-value, ideal cho dictionary locators/results."
        },
        {
          "q": "HashMap vs TreeMap — khi cần keys sorted alphabetically?",
          "options": [
            "TreeMap",
            "HashMap",
            "ArrayList",
            "HashSet"
          ],
          "answer": 0,
          "explain": "TreeMap = Red-Black tree, keys sorted."
        },
        {
          "q": "list.add(0, x) trên ArrayList có đặc điểm performance?",
          "options": [
            "O(n) do shift elements",
            "O(1)",
            "O(log n)",
            "Không hỗ trợ"
          ],
          "answer": 0,
          "explain": "Insert giữa/cuối ArrayList tốn chi phí dịch phần tử."
        },
        {
          "q": "Khi lưu danh sách test case ID không trùng, collection phù hợp?",
          "options": [
            "Set (HashSet)",
            "List",
            "Queue",
            "Stack"
          ],
          "answer": 0,
          "explain": "Set đảm bảo uniqueness."
        },
        {
          "q": "ConcurrentModificationException thường gặp khi?",
          "options": [
            "Modify collection while iterating không qua Iterator.remove",
            "Dùng HashMap",
            "Dùng ArrayList.get",
            "Compile error"
          ],
          "answer": 0,
          "explain": "Cấu trúc bị đổi trong lúc for-each — dùng Iterator hoặc copy."
        },
        {
          "q": "Map.get(key) trả về null — luôn có nghĩa key không tồn tại?",
          "options": [
            "Không — có thể value thực sự là null",
            "Luôn không tồn tại",
            "Luôn lỗi",
            "Map không cho null value"
          ],
          "answer": 0,
          "explain": "containsKey() để phân biệt missing key vs null value."
        },
        {
          "q": "LinkedList implements List và Deque — ứng dụng queue test jobs?",
          "options": [
            "Có — addLast/pollFirst cho FIFO queue",
            "Không — chỉ ArrayList",
            "Chỉ HashSet",
            "Chỉ TreeMap"
          ],
          "answer": 0,
          "explain": "Deque interface hỗ trợ queue/stack operations."
        },
        {
          "q": "Collections.sort(list) yêu cầu elements?",
          "options": [
            "Comparable hoặc truyền Comparator",
            "Phải là String",
            "Phải unique",
            "Phải HashMap"
          ],
          "answer": 0,
          "explain": "Sort cần cách so sánh — Comparable/Comparator."
        },
        {
          "q": "HashMap internal: collision xử lý (Java 8+) bằng?",
          "options": [
            "Linked list / tree tại bucket khi nhiều key cùng hash",
            "Bỏ qua key trùng",
            "Copy sang ArrayList",
            "Throw error"
          ],
          "answer": 0,
          "explain": "Bucket chaining; treeify khi chain dài."
        },
        {
          "q": "Chọn structure lưu kết quả test run: testName → PASS/FAIL?",
          "options": [
            "Map<String, String>",
            "Set",
            "Stack",
            "Queue"
          ],
          "answer": 0,
          "explain": "Map phù hợp key-value results."
        },
        {
          "q": "ArrayList(initialCapacity) lợi ích khi biết trước size?",
          "options": [
            "Giảm resize internal array, tăng performance",
            "Tự động sort",
            "Unique elements",
            "Thread-safe"
          ],
          "answer": 0,
          "explain": "Tránh grow nhiều lần khi biết kích thước ước lượng."
        },
        {
          "q": "Immutable list (List.of) lợi ích trong framework?",
          "options": [
            "An toàn, không bị test code sửa nhầm constants",
            "Nhanh hơn ArrayList mutable",
            "Cho phép null mọi nơi",
            "Tự động thread-safe mọi case"
          ],
          "answer": 0,
          "explain": "Immutable collections bảo vệ config/constants."
        },
        {
          "q": "contains() trên List complexity?",
          "options": [
            "O(n) linear search",
            "O(1)",
            "O(log n)",
            "O(n log n)"
          ],
          "answer": 0,
          "explain": "List.contains phải duyệt — Set/Map hash O(1) average."
        },
        {
          "q": "PriorityQueue dùng khi automation cần?",
          "options": [
            "Process jobs theo priority (severity, deadline)",
            "Unique elements",
            "Key-value",
            "Sorted map keys"
          ],
          "answer": 0,
          "explain": "PriorityQueue = heap theo comparator."
        },
        {
          "q": "equals() và hashCode() contract cho HashMap key?",
          "options": [
            "Equal objects phải cùng hashCode; cùng hash có thể khác equal",
            "Không liên quan",
            "Chỉ cần equals",
            "Chỉ cần hashCode"
          ],
          "answer": 0,
          "explain": "Vi phạm contract gây mất entry trong HashMap."
        },
        {
          "q": "Copy List trước khi iterate để modify an toàn bằng?",
          "options": [
            "new ArrayList<>(original) hoặc List.copyOf",
            "original.clear()",
            "Collections.reverse",
            "Không thể"
          ],
          "answer": 0,
          "explain": "Snapshot copy tránh ConcurrentModification."
        },
        {
          "q": "Trong interview: khi nào List, Set, Map?",
          "options": [
            "List: ordered/duplicate; Set: unique; Map: lookup by key",
            "Luôn ArrayList",
            "Luôn HashMap",
            "Không dùng Collections Framework"
          ],
          "answer": 0,
          "explain": "Chọn theo semantics dữ liệu, không theo thói quen."
        },
        {
          "q": "Stream API (preview Collections) — forEach trên List test IDs để?",
          "options": [
            "Duyệt functional style; có thể filter/map",
            "Sort only",
            "Replace HashMap",
            "Compile-time only"
          ],
          "answer": 0,
          "explain": "Streams xử lý collection declarative — liên kết JC3."
        }
      ]
    },
    "java34": {
      "title": "Advanced Java",
      "questions": [
        {
          "q": "finally block chạy khi nào?",
          "options": [
            "Luôn (trừ System.exit) sau try/catch",
            "Chỉ khi có exception",
            "Chỉ khi không exception",
            "Không bao giờ"
          ],
          "answer": 0,
          "explain": "finally dùng đóng resource (driver, file)."
        },
        {
          "q": "checked vs unchecked exception?",
          "options": [
            "Checked: compile bắt buộc handle; Unchecked: RuntimeException",
            "Giống nhau",
            "Unchecked phải throws",
            "Checked không cần try"
          ],
          "answer": 0,
          "explain": "IOException checked; NullPointerException unchecked."
        },
        {
          "q": "try-with-resources yêu cầu resource?",
          "options": [
            "Implement AutoCloseable",
            "Extend Thread",
            "static",
            "final"
          ],
          "answer": 0,
          "explain": "Tự đóng close() — best practice File/Reader/Stream."
        },
        {
          "q": "custom exception nên extend?",
          "options": [
            "Exception hoặc RuntimeException tùy strategy",
            "Object",
            "String",
            "Thread"
          ],
          "answer": 0,
          "explain": "Business exception thường RuntimeException nếu không force catch."
        },
        {
          "q": "Stream filter + map pipeline đọc file lines để?",
          "options": [
            "Transform/lọc declarative",
            "Thay for-loop bắt buộc",
            "Chỉ sort",
            "Chỉ write file"
          ],
          "answer": 0,
          "explain": "Stream = map/filter/collect trên collection."
        },
        {
          "q": "Lambda (x) -> x*2 dùng với?",
          "options": [
            "Functional interface (một abstract method)",
            "Mọi class",
            "static method only",
            "Constructor"
          ],
          "answer": 0,
          "explain": "Lambda = shorthand cho SAM interface."
        },
        {
          "q": "Optional.ofNullable tránh?",
          "options": [
            "NullPointerException khi chain",
            "IOException",
            "Compile error",
            "Infinite loop"
          ],
          "answer": 0,
          "explain": "Optional thể hiện có/không value."
        },
        {
          "q": "Files.readString(path) thuộc?",
          "options": [
            "java.nio.file modern I/O",
            "java.applet",
            "Collections",
            "Thread"
          ],
          "answer": 0,
          "explain": "NIO.2 API đọc file gọn."
        },
        {
          "q": "throw vs throws?",
          "options": [
            "throw: ném tại chỗ; throws: khai báo method có thể ném",
            "Giống nhau",
            "throws ném ngay",
            "throw chỉ compile"
          ],
          "answer": 0,
          "explain": "Phân biệt hay hỏi interview."
        },
        {
          "q": "catch (Exception e) quá rộng — vấn đề?",
          "options": [
            "Nuốt lỗi cụ thể, khó debug",
            "Nhanh hơn",
            "Bắt buộc",
            "Tốt nhất"
          ],
          "answer": 0,
          "explain": "Catch specific trước, Exception cuối nếu cần."
        },
        {
          "q": "parallelStream() rủi ro trong test?",
          "options": [
            "Race condition, không deterministic",
            "Luôn nhanh hơn",
            "Không dùng được",
            "Chỉ cho List"
          ],
          "answer": 0,
          "explain": "Parallel cần thread-safe data."
        },
        {
          "q": "Predicate<T> trong Stream dùng để?",
          "options": [
            "Test condition filter",
            "Map transform",
            "Reduce sum",
            "Sort"
          ],
          "answer": 0,
          "explain": "Predicate = boolean test."
        },
        {
          "q": "BufferedReader giúp?",
          "options": [
            "Đọc theo buffer, hiệu quả hơn từng byte",
            "Ghi file",
            "Network only",
            "Compile"
          ],
          "answer": 0,
          "explain": "Buffer giảm I/O calls."
        },
        {
          "q": "multi-catch catch (A | B e) lợi ích?",
          "options": [
            "Một block xử lý nhiều type",
            "Chậm hơn",
            "Không compile",
            "Thay throws"
          ],
          "answer": 0,
          "explain": "Java 7+ gọn hơn nhiều catch giống nhau."
        },
        {
          "q": "AssertionError vs Exception trong test?",
          "options": [
            "AssertionError thường từ assert/TestNG assert",
            "Giống nhau",
            "Luôn checked",
            "Không trong Java"
          ],
          "answer": 0,
          "explain": "Assert fail = AssertionError/AssertionError tùy framework."
        },
        {
          "q": "String không đổi (immutable) ảnh hưởng?",
          "options": [
            "An toàn thread; nối nhiều dùng StringBuilder",
            "Không hash được",
            "Không equals",
            "Không dùng được"
          ],
          "answer": 0,
          "explain": "Immutable string — dùng builder khi loop concat."
        },
        {
          "q": "collect(Collectors.toList()) sau stream?",
          "options": [
            "Materialize stream thành List",
            "Sort in-place",
            "Filter only",
            "Close file"
          ],
          "answer": 0,
          "explain": "Terminal operation tạo collection."
        },
        {
          "q": "FileNotFoundException thường?",
          "options": [
            "Checked — phải handle khi đọc file",
            "Unchecked",
            "Runtime only",
            "Không trong Java"
          ],
          "answer": 0,
          "explain": "IO checked exception classic."
        },
        {
          "q": "method reference Class::method dùng khi?",
          "options": [
            "Lambda chỉ gọi một method có sẵn",
            "Cần loop",
            "Cần 3+ statements",
            "Thay class"
          ],
          "answer": 0,
          "explain": "Shorthand khi logic đơn giản."
        },
        {
          "q": "try-catch trong @Test nên?",
          "options": [
            "Tránh — để TestNG/framework báo fail rõ",
            "Luôn catch Exception pass",
            "Không bao giờ assert",
            "Bỏ finally"
          ],
          "answer": 0,
          "explain": "Test fail nên qua assertion, không nuốt exception."
        }
      ]
    },
    "video1": {
      "title": "Manual vs Automation",
      "questions": [
        {
          "q": "Automation testing phù hợp khi?",
          "options": [
            "Regression lớn, stable app, ROI dương dài hạn",
            "Mọi exploratory test",
            "UI thay đổi hàng ngày",
            "Không cần maintain"
          ],
          "answer": 0,
          "explain": "Không automate hết — chọn case ổn định, lặp lại."
        },
        {
          "q": "Test Pyramid khuyến nghị tỷ lệ?",
          "options": [
            "Nhiều unit, ít E2E",
            "Nhiều E2E, ít unit",
            "Chỉ manual",
            "Chỉ API"
          ],
          "answer": 0,
          "explain": "Pyramid: unit base rộng, UI E2E đỉnh nhỏ."
        },
        {
          "q": "Flaky test là gì?",
          "options": [
            "Pass/fail không nhất quán cùng code",
            "Test chậm",
            "Test manual",
            "Test unit"
          ],
          "answer": 0,
          "explain": "Flaky = timing/data/env — enemy của CI."
        },
        {
          "q": "ROI automation âm khi nào?",
          "options": [
            "Maintain script > tiết kiệm thời gian",
            "Chạy parallel",
            "Dùng POM",
            "Dùng CI"
          ],
          "answer": 0,
          "explain": "ROI = (manual cost saved) - (automation cost)."
        },
        {
          "q": "Manual testing vẫn cần cho?",
          "options": [
            "Exploratory, usability, ad-hoc",
            "Regression 1000 case",
            "Load test",
            "Nightly build"
          ],
          "answer": 0,
          "explain": "Automation không thay sáng tạo và UX exploration."
        },
        {
          "q": "Record & playback tool hạn chế?",
          "options": [
            "Script brittle, khó maintain khi UI đổi",
            "Không chạy được",
            "Không free",
            "Không record"
          ],
          "answer": 0,
          "explain": "Low-code record thường break khi locator đổi."
        },
        {
          "q": "Definition of Done cho automation story?",
          "options": [
            "Script + code review + CI green + doc",
            "Chỉ record video",
            "Chỉ chạy local",
            "Không cần assert"
          ],
          "answer": 0,
          "explain": "DoD gồm maintainability và CI."
        },
        {
          "q": "Shift-left testing nghĩa là?",
          "options": [
            "Test sớm hơn trong SDLC (unit, API sớm)",
            "Test production only",
            "Chỉ manual",
            "Chỉ UAT"
          ],
          "answer": 0,
          "explain": "Shift-left = phát hiện lỗi sớm, rẻ hơn."
        },
        {
          "q": "Automation engineer vs manual — skill khác?",
          "options": [
            "Coding, framework, CI; manual: domain, exploration",
            "Giống hệt",
            "Manual cần Java bắt buộc",
            "Automation không cần logic"
          ],
          "answer": 0,
          "explain": "Automation = dev-test hybrid."
        },
        {
          "q": "Khi UI unstable, chiến lược?",
          "options": [
            "API/contract test trước, UI sau khi stable",
            "Automate hết UI ngay",
            "Bỏ test",
            "Chỉ screenshot"
          ],
          "answer": 0,
          "explain": "Test layer phù hợp độ ổn định."
        },
        {
          "q": "Smoke suite automation mục tiêu?",
          "options": [
            "Xác nhận build deployable nhanh",
            "Full regression",
            "Performance",
            "Security scan"
          ],
          "answer": 0,
          "explain": "Smoke = critical path ngắn."
        },
        {
          "q": "Maintainability automation phụ thuộc?",
          "options": [
            "POM, clean code, locator strategy",
            "Số lượng test nhiều",
            "Ít comment",
            "Record only"
          ],
          "answer": 0,
          "explain": "Design quan trọng hơn số lượng."
        },
        {
          "q": "False positive trong test?",
          "options": [
            "Pass nhưng app thực tế lỗi",
            "Fail đúng",
            "Timeout",
            "Skip"
          ],
          "answer": 0,
          "explain": "Assert yếu → false positive nguy hiểm."
        },
        {
          "q": "CI chạy automation khi?",
          "options": [
            "Mỗi commit/PR/nightly theo chiến lược",
            "Chỉ cuối năm",
            "Chỉ manual trigger",
            "Không cần"
          ],
          "answer": 0,
          "explain": "CI = fast feedback loop."
        },
        {
          "q": "Data-driven manual vs automation?",
          "options": [
            "Automation scale data dễ hơn",
            "Manual luôn nhanh hơn",
            "Không dùng data",
            "Chỉ CSV"
          ],
          "answer": 0,
          "explain": "Automation + data file = hàng trăm case."
        },
        {
          "q": "Không nên automate 100% vì?",
          "options": [
            "Một số test không ROI, cần human judgment",
            "Tool không đủ",
            "Java không hỗ trợ",
            "Agile cấm"
          ],
          "answer": 0,
          "explain": "100% automation là anti-pattern thường gặp."
        },
        {
          "q": "Version control cho test code?",
          "options": [
            "Bắt buộc — Git như production code",
            "Không cần",
            "Chỉ screenshot",
            "Chỉ Excel"
          ],
          "answer": 0,
          "explain": "Test code là code — cần VCS."
        },
        {
          "q": "Stakeholder cần báo cáo automation?",
          "options": [
            "Coverage, pass rate, duration, flaky",
            "Chỉ số dòng code",
            "Không báo cáo",
            "Chỉ log console"
          ],
          "answer": 0,
          "explain": "Metrics minh bạch giá trị automation."
        },
        {
          "q": "Reusable component trong framework?",
          "options": [
            "Giảm duplicate, tăng maintain",
            "Tăng flaky",
            "Chậm hơn",
            "Không cần OOP"
          ],
          "answer": 0,
          "explain": "Reuse = core engineering practice."
        },
        {
          "q": "Entry criteria chạy automation suite?",
          "options": [
            "Env stable, data ready, build deploy OK",
            "Không cần",
            "Chỉ khi release",
            "Random"
          ],
          "answer": 0,
          "explain": "Precondition rõ — tránh fail mơ hồ."
        }
      ]
    },
    "video2": {
      "title": "4 Loại Test",
      "questions": [
        {
          "q": "Unit test đặc điểm?",
          "options": [
            "Cô lập module nhỏ, nhanh, mock dependency",
            "Cần browser",
            "Cần DB thật",
            "Chỉ manual"
          ],
          "answer": 0,
          "explain": "Unit = isolated, fast feedback."
        },
        {
          "q": "Integration test kiểm tra?",
          "options": [
            "Tương tác giữa module/service",
            "Chỉ một method",
            "Chỉ UI pixel",
            "Chỉ document"
          ],
          "answer": 0,
          "explain": "Integration = boundary giữa components."
        },
        {
          "q": "E2E test trong web?",
          "options": [
            "Luồng user thật qua UI (hoặc gần production)",
            "Chỉ unit",
            "Chỉ SQL",
            "Không cần assert"
          ],
          "answer": 0,
          "explain": "E2E = full stack user journey."
        },
        {
          "q": "API test thường nhanh hơn UI E2E vì?",
          "options": [
            "Không render browser, ít flaky",
            "Không cần assert",
            "Không cần data",
            "Luôn manual"
          ],
          "answer": 0,
          "explain": "API layer ổn định hơn UI cho regression."
        },
        {
          "q": "Test isolation unit test dùng?",
          "options": [
            "Mock/stub dependency",
            "Browser thật",
            "Production DB",
            "Không cần"
          ],
          "answer": 0,
          "explain": "Mock = kiểm soát behavior dependency."
        },
        {
          "q": "Contract test (API) đảm bảo?",
          "options": [
            "Consumer/provider thỏa agreement",
            "UI color",
            "CPU usage",
            "Manual only"
          ],
          "answer": 0,
          "explain": "Contract = schema/response agreement."
        },
        {
          "q": "Regression suite nên gồm?",
          "options": [
            "Mix unit + integration + critical E2E",
            "Chỉ exploratory",
            "Chỉ một unit test",
            "Không API"
          ],
          "answer": 0,
          "explain": "Pyramid shape cho regression."
        },
        {
          "q": "Performance test khác functional?",
          "options": [
            "Đo latency/throughput dưới load",
            "Cùng loại",
            "Chỉ manual",
            "Chỉ UI"
          ],
          "answer": 0,
          "explain": "Performance = non-functional."
        },
        {
          "q": "Security test (basic) trong API?",
          "options": [
            "AuthZ, injection, sensitive data leak",
            "Chỉ status 200",
            "Chỉ UI",
            "Không thuộc test"
          ],
          "answer": 0,
          "explain": "Security là loại test riêng nhưng hay gộp API."
        },
        {
          "q": "Smoke vs Sanity?",
          "options": [
            "Smoke: rộng shallow; Sanity: hẹp sau fix",
            "Giống nhau",
            "Ngược hoàn toàn",
            "Không dùng"
          ],
          "answer": 0,
          "explain": "Thuật ngữ hay nhầm — phỏng vấn hay hỏi."
        },
        {
          "q": "Test double là gì?",
          "options": [
            "Mock, stub, fake thay dependency",
            "Hai assertion",
            "Hai browser",
            "Hai CI"
          ],
          "answer": 0,
          "explain": "General term cho fake collaborators."
        },
        {
          "q": "E2E ít nhưng quan trọng vì?",
          "options": [
            "Chậm, flaky hơn nhưng bắt integration gap",
            "Không cần",
            "Thay unit",
            "Free"
          ],
          "answer": 0,
          "explain": "Ít E2E critical path, không bỏ hẳn."
        },
        {
          "q": "API regression sau deploy backend?",
          "options": [
            "Chạy trước/song song UI — fail sớm",
            "Không cần",
            "Chỉ manual",
            "Chỉ unit"
          ],
          "answer": 0,
          "explain": "API fail thường rẻ hơn để fix sớm."
        },
        {
          "q": "Component test (middle layer)?",
          "options": [
            "Giữa unit và E2E — module vài phần ghép",
            "Chỉ production",
            "Chỉ load",
            "Không tồn tại"
          ],
          "answer": 0,
          "explain": "Integration/component hay dùng interchangeably."
        },
        {
          "q": "Test data cho integration?",
          "options": [
            "Có thể DB test env, seed controlled",
            "Luôn production",
            "Không data",
            "Random only"
          ],
          "answer": 0,
          "explain": "Controlled test data giảm flaky."
        },
        {
          "q": "Shift-right (production monitoring)?",
          "options": [
            "Test/learn từ prod telemetry",
            "Thay unit test",
            "Chỉ manual",
            "Không liên quan"
          ],
          "answer": 0,
          "explain": "Bổ sung pyramid — observability."
        },
        {
          "q": "Negative testing API ví dụ?",
          "options": [
            "Invalid body → 400, wrong auth → 401",
            "Chỉ happy path 200",
            "Không assert status",
            "Chỉ UI"
          ],
          "answer": 0,
          "explain": "Negative = security/robustness."
        },
        {
          "q": "Unit test naming convention?",
          "options": [
            "method_condition_expected",
            "test1",
            "a",
            "Không tên"
          ],
          "answer": 0,
          "explain": "Tên rõ giúp debug CI fail."
        },
        {
          "q": "Khi nào ưu tiên API over UI automation?",
          "options": [
            "Service stable, UI đổi layout thường xuyên",
            "Luôn UI",
            "Không bao giờ API",
            "Chỉ manual"
          ],
          "answer": 0,
          "explain": "Layer chọn theo stability và ROI."
        },
        {
          "q": "4 loại test trong khóa — thứ tự execute CI điển hình?",
          "options": [
            "Unit → API/Integration → E2E smoke",
            "E2E trước unit",
            "Chỉ manual",
            "Random"
          ],
          "answer": 0,
          "explain": "Fail fast: rẻ trước, đắt sau."
        }
      ]
    },
    "phase2": {
      "title": "Selenium WebDriver",
      "questions": [
        {
          "q": "WebDriver khác WebDriverManager?",
          "options": [
            "Driver = API; Manager tải driver binary phù hợp browser",
            "Giống nhau",
            "Manager thay Selenium",
            "Driver chỉ Firefox"
          ],
          "answer": 0,
          "explain": "Manager giải pain version chromedriver."
        },
        {
          "q": "By.id() ưu tiên vì?",
          "options": [
            "Thường unique, nhanh, ít brittle nhất",
            "Luôn chậm",
            "Bắt buộc XPath",
            "Không stable"
          ],
          "answer": 0,
          "explain": "Locator priority: id > name > css > xpath."
        },
        {
          "q": "XPath //button[@type='submit'] là?",
          "options": [
            "XPath tuyệt đối tìm button attribute",
            "CSS",
            "ID",
            "Link text"
          ],
          "answer": 0,
          "explain": "XPath mạnh nhưng dễ fragile nếu DOM sâu."
        },
        {
          "q": "Implicit wait 10s nghĩa là?",
          "options": [
            "Mỗi findElement chờ tối đa 10s nếu chưa có",
            "Chỉ một lần",
            "Chỉ explicit",
            "Không chờ"
          ],
          "answer": 0,
          "explain": "Implicit global — có thể làm test chậm nếu lạm dụng."
        },
        {
          "q": "Explicit wait WebDriverWait dùng?",
          "options": [
            "ExpectedCondition cụ thể (visible, clickable)",
            "Thread.sleep only",
            "Implicit only",
            "Không wait"
          ],
          "answer": 0,
          "explain": "Explicit = best practice chờ điều kiện."
        },
        {
          "q": "Thread.sleep trong test?",
          "options": [
            "Anti-pattern — flaky và lãng phí",
            "Best practice",
            "Thay explicit",
            "Bắt buộc"
          ],
          "answer": 0,
          "explain": "Hard sleep = không biết điều kiện thật."
        },
        {
          "q": "NoSuchElementException thường do?",
          "options": [
            "Locator sai hoặc element chưa xuất hiện",
            "Network down",
            "Java version",
            "TestNG"
          ],
          "answer": 0,
          "explain": "Fix: locator + wait + iframe."
        },
        {
          "q": "driver.findElement trả về?",
          "options": [
            "WebElement",
            "WebDriver",
            "List always",
            "String"
          ],
          "answer": 0,
          "explain": "Single element — findElements cho list."
        },
        {
          "q": "sendKeys vs click?",
          "options": [
            "sendKeys nhập text; click tương tác",
            "Giống nhau",
            "Ngược",
            "Không dùng"
          ],
          "answer": 0,
          "explain": "Basic interaction API."
        },
        {
          "q": "getAttribute('value') lấy?",
          "options": [
            "Giá trị attribute HTML (value, href...)",
            "Text visible",
            "CSS color",
            "Cookie"
          ],
          "answer": 0,
          "explain": "Attribute vs getText() khác nhau."
        },
        {
          "q": "switchTo().frame() khi nào?",
          "options": [
            "Element nằm trong iframe",
            "Mọi trang",
            "Sau alert",
            "Không cần"
          ],
          "answer": 0,
          "explain": "Phải switch context vào frame."
        },
        {
          "q": "Alert accept/dismiss dùng?",
          "options": [
            "driver.switchTo().alert()",
            "findElement By.id",
            "Actions only",
            "Javascript only"
          ],
          "answer": 0,
          "explain": "Alert là window riêng — switch alert."
        },
        {
          "q": "Actions class doubleClick dùng cho?",
          "options": [
            "Hover, drag-drop, double-click phức tạp",
            "Chỉ navigate",
            "Chỉ cookie",
            "Thay assert"
          ],
          "answer": 0,
          "explain": "Actions = low-level interaction chain."
        },
        {
          "q": "Page Object Model lợi ích?",
          "options": [
            "Tách locator/logic UI, reuse, maintain",
            "Chậm hơn",
            "Không OOP",
            "Thay TestNG"
          ],
          "answer": 0,
          "explain": "POM = design pattern cho Selenium."
        },
        {
          "q": "CSS selector #login-btn là?",
          "options": [
            "ID login-btn",
            "Class only",
            "XPath",
            "Name"
          ],
          "answer": 0,
          "explain": "# = id trong CSS selector."
        },
        {
          "q": "StaleElementReferenceException?",
          "options": [
            "Element DOM đã refresh, reference cũ invalid",
            "Locator sai",
            "Timeout",
            "Cookie"
          ],
          "answer": 0,
          "explain": "Re-find element sau navigation/refresh."
        },
        {
          "q": "Headless Chrome lợi ích CI?",
          "options": [
            "Chạy không UI, phù hợp server",
            "Không chạy được",
            "Chậm hơn luôn",
            "Không screenshot"
          ],
          "answer": 0,
          "explain": "Headless = CI standard."
        },
        {
          "q": "driver.get(url) vs navigate().to()?",
          "options": [
            "Cả hai mở URL — tương đương thực tế",
            "Khác hoàn toàn",
            "Chỉ get",
            "Chỉ navigate"
          ],
          "answer": 0,
          "explain": "get phổ biến; navigate part of Navigation interface."
        },
        {
          "q": "Screenshot on failure thường ở đâu?",
          "options": [
            "@AfterMethod listener / try-catch TestNG",
            "Trong @BeforeSuite only",
            "Không cần",
            "Manual only"
          ],
          "answer": 0,
          "explain": "Hook after test fail — phase4 sâu hơn."
        },
        {
          "q": "findElements size 0 nghĩa là?",
          "options": [
            "Không tìm thấy (empty list), không throw",
            "Exception luôn",
            "Tìm thấy một",
            "Bug Selenium"
          ],
          "answer": 0,
          "explain": "findElements an toàn khi có thể 0."
        }
      ]
    },
    "phase3": {
      "title": "TestNG & POM",
      "questions": [
        {
          "q": "@Test trong TestNG?",
          "options": [
            "Đánh dấu method là test case",
            "Before suite",
            "Data provider only",
            "Listener"
          ],
          "answer": 0,
          "explain": "@Test = executable test method."
        },
        {
          "q": "@BeforeMethod chạy?",
          "options": [
            "Trước mỗi @Test method",
            "Một lần suite",
            "Sau test",
            "Không bao giờ"
          ],
          "answer": 0,
          "explain": "Setup per test — driver init thường ở đây."
        },
        {
          "q": "testng.xml dùng để?",
          "options": [
            "Khai báo suite, groups, parallel, listeners",
            "Viết locator",
            "Thay pom.xml",
            "Compile Java"
          ],
          "answer": 0,
          "explain": "XML điều khiển execution TestNG."
        },
        {
          "q": "@DataProvider trả về?",
          "options": [
            "Object[][] hoặc Iterator cho parameterized test",
            "String only",
            "void only",
            "WebDriver"
          ],
          "answer": 0,
          "explain": "Data-driven nhiều row data một test."
        },
        {
          "q": "dependsOnMethods?",
          "options": [
            "Test phụ thuộc test khác pass trước",
            "Parallel only",
            "Skip assert",
            "Group only"
          ],
          "answer": 0,
          "explain": "Order dependency — dùng cẩn thận."
        },
        {
          "q": "groups trong TestNG?",
          "options": [
            "Chạy subset smoke/regression",
            "Package name",
            "Maven profile only",
            "Không có"
          ],
          "answer": 0,
          "explain": "groups=smoke trên @Test và xml."
        },
        {
          "q": "POM: LoginPage extends BasePage lợi ích?",
          "options": [
            "Chia trách nhiệm từng trang",
            "Một class 5000 dòng",
            "Không cần driver",
            "Thay TestNG"
          ],
          "answer": 0,
          "explain": "Mỗi page một class — SRP."
        },
        {
          "q": "PageFactory @FindBy?",
          "options": [
            "Lazy init element khi dùng",
            "Eager only",
            "Thay driver",
            "Không Selenium"
          ],
          "answer": 0,
          "explain": "FindBy giảm boilerplate locator."
        },
        {
          "q": "Assert.assertEquals vs TestNG Assert?",
          "options": [
            "TestNG assert có message, integration report",
            "Không khác",
            "JUnit only",
            "Không assert"
          ],
          "answer": 0,
          "explain": "Assertions = verify expected."
        },
        {
          "q": "soft assert (SoftAssert)?",
          "options": [
            "Gom lỗi, assertAll() cuối",
            "Dừng ngay lỗi đầu",
            "Không TestNG",
            "Thay hard assert"
          ],
          "answer": 0,
          "explain": "Soft assert cho nhiều check một test."
        },
        {
          "q": "parallel='methods' trong xml?",
          "options": [
            "Chạy test methods song song",
            "Sequential only",
            "Chỉ class",
            "Không xml"
          ],
          "answer": 0,
          "explain": "Parallel cần thread-safe driver factory."
        },
        {
          "q": "@AfterMethod alwaysRun?",
          "options": [
            "Chạy cả khi test fail — quit driver",
            "Không chạy khi fail",
            "Chỉ pass",
            "Before test"
          ],
          "answer": 0,
          "explain": "Cleanup driver bắt buộc alwaysRun=true."
        },
        {
          "q": "InvocationCount=5?",
          "options": [
            "Chạy cùng test 5 lần",
            "5 thread",
            "5 browser",
            "5 suite"
          ],
          "answer": 0,
          "explain": "Dùng stress nhẹ hoặc flaky check."
        },
        {
          "q": "priority trong @Test?",
          "options": [
            "Thứ tự trong cùng class (không khuyến khích lạm dụng)",
            "Parallel level",
            "Group name",
            "Data row"
          ],
          "answer": 0,
          "explain": "priority thay dependsOn khi đơn giản."
        },
        {
          "q": "BaseTest chứa?",
          "options": [
            "driver setup/teardown, common config",
            "Tất cả locator app",
            "Production code",
            "Không nên"
          ],
          "answer": 0,
          "explain": "Base class DRY cho test infrastructure."
        },
        {
          "q": "Maven surefire + TestNG?",
          "options": [
            "Maven chạy TestNG khi mvn test",
            "Chỉ IDE",
            "Chỉ manual",
            "Không build"
          ],
          "answer": 0,
          "explain": "surefire plugin bind test phase."
        },
        {
          "q": "Listener onTestFailure?",
          "options": [
            "Screenshot, log, custom report",
            "Skip test",
            "Compile",
            "Data provider"
          ],
          "answer": 0,
          "explain": "Listener hook lifecycle TestNG."
        },
        {
          "q": "Page object không nên assert?",
          "options": [
            "Nên assert ở test layer; page trả state",
            "Assert trong mọi method",
            "Không assert bao giờ",
            "Chỉ trong xml"
          ],
          "answer": 0,
          "explain": "Debate: page có thể có isLoaded(); test quyết định pass."
        },
        {
          "q": "@Parameters đọc từ?",
          "options": [
            "testng.xml <parameter>",
            "application.properties only",
            "Env only",
            "Không hỗ trợ"
          ],
          "answer": 0,
          "explain": "XML parameters cho environment."
        },
        {
          "q": "RetryAnalyzer (preview phase4)?",
          "options": [
            "Tự chạy lại test fail",
            "Skip fail",
            "Double assert",
            "Không TestNG"
          ],
          "answer": 0,
          "explain": "Retry giảm flaky noise — config cẩn thận."
        }
      ]
    },
    "phase4": {
      "title": "Advanced & CI/CD",
      "questions": [
        {
          "q": "Listener ITestListener dùng?",
          "options": [
            "Hook pass/fail/skip events",
            "Locator",
            "Maven",
            "CSS"
          ],
          "answer": 0,
          "explain": "Listener = cross-cutting test behavior."
        },
        {
          "q": "Retry failed test risk?",
          "options": [
            "Che giấu bug thật nếu retry quá nhiều",
            "Luôn tốt",
            "Không retry được",
            "Chỉ manual"
          ],
          "answer": 0,
          "explain": "Retry có điều kiện + log."
        },
        {
          "q": "Cross-browser testing nghĩa?",
          "options": [
            "Chrome, Firefox, Edge — matrix",
            "Chỉ Chrome",
            "Chỉ headless",
            "Không Selenium"
          ],
          "answer": 0,
          "explain": "Grid/Cloud cho multi browser."
        },
        {
          "q": "Jenkins pipeline stage test?",
          "options": [
            "Build → Test → Deploy với gate",
            "Chỉ email",
            "Chỉ git",
            "Không CI"
          ],
          "answer": 0,
          "explain": "Pipeline as code — fail build nếu test fail."
        },
        {
          "q": "Screenshot file naming?",
          "options": [
            "timestamp_testName để unique",
            "fixed.png only",
            "Không lưu",
            "Chỉ log"
          ],
          "answer": 0,
          "explain": "Unique name tránh overwrite."
        },
        {
          "q": "Log4j/SLF4J trong framework?",
          "options": [
            "Structured log debug CI fail",
            "Thay assert",
            "Thay driver",
            "Không cần"
          ],
          "answer": 0,
          "explain": "Log + screenshot = triage nhanh."
        },
        {
          "q": "Flaky test mitigation?",
          "options": [
            "Explicit wait, stable locator, retry có kiểm soát",
            "sleep random",
            "Bỏ assert",
            "Chỉ chạy local"
          ],
          "answer": 0,
          "explain": "Flaky = địch CI ổn định."
        },
        {
          "q": "ThreadLocal WebDriver?",
          "options": [
            "Mỗi thread parallel có driver riêng",
            "Một driver global",
            "Không parallel",
            "Không Java"
          ],
          "answer": 0,
          "explain": "ThreadLocal pattern cho parallel TestNG."
        },
        {
          "q": "ExtentReport/Allure?",
          "options": [
            "HTML/report đẹp cho stakeholder",
            "Thay TestNG",
            "Thay Selenium",
            "Không report"
          ],
          "answer": 0,
          "explain": "Reporting = communication."
        },
        {
          "q": "Grid Selenium?",
          "options": [
            "Remote hub/node chạy browser từ xa",
            "Local only",
            "API only",
            "Không distribute"
          ],
          "answer": 0,
          "explain": "Grid scale browsers."
        },
        {
          "q": "Docker trong CI test?",
          "options": [
            "Consistent env, agent có browser image",
            "Thay Java",
            "Không cần",
            "Chỉ production"
          ],
          "answer": 0,
          "explain": "Container hóa test env."
        },
        {
          "q": "Failed test triage order?",
          "options": [
            "Log → screenshot → reproduce local",
            "Delete test",
            "Retry forever",
            "Ignore"
          ],
          "answer": 0,
          "explain": "Quy trình debug có hệ thống."
        },
        {
          "q": "@Factory trong TestNG?",
          "options": [
            "Tạo test instances dynamic",
            "Data provider",
            "Listener",
            "Maven"
          ],
          "answer": 0,
          "explain": "Factory advanced dynamic tests."
        },
        {
          "q": "Build pipeline fail on test?",
          "options": [
            "Quality gate — không deploy nếu đỏ",
            "Luôn deploy",
            "Không chạy test",
            "Chỉ warning"
          ],
          "answer": 0,
          "explain": "CI gate bảo vệ production."
        },
        {
          "q": "Environment variable trong CI?",
          "options": [
            "BASE_URL, CREDENTIALS từ Jenkins secrets",
            "Hardcode prod",
            "Không config",
            "Chỉ xml"
          ],
          "answer": 0,
          "explain": "Config externalized — 12-factor."
        },
        {
          "q": "Video recording test?",
          "options": [
            "Debug intermittent — tốn disk",
            "Bắt buộc",
            "Thay screenshot",
            "Không có tool"
          ],
          "answer": 0,
          "explain": "Video optional cho flaky E2E."
        },
        {
          "q": "Parallel classes vs methods?",
          "options": [
            "classes: mỗi class thread; methods: finer grain",
            "Giống nhau",
            "Không parallel",
            "Chỉ suite"
          ],
          "answer": 0,
          "explain": "Chọn parallel level theo isolation."
        },
        {
          "q": "Quarantine flaky tests?",
          "options": [
            "Tách suite unstable, fix riêng",
            "Xóa hết",
            "Retry vô hạn",
            "Không chạy CI"
          ],
          "answer": 0,
          "explain": "Quarantine giữ CI xanh trong khi fix."
        },
        {
          "q": "Definition CI vs CD?",
          "options": [
            "CI: integrate+test; CD: deploy automated",
            "Giống nhau",
            "Chỉ manual",
            "Chỉ unit"
          ],
          "answer": 0,
          "explain": "CI/CD hay đi cùng pipeline."
        },
        {
          "q": "Best practice secret trong repo?",
          "options": [
            "Không commit — dùng vault/env",
            "Commit cho tiện",
            "Hardcode OK",
            "Share chat"
          ],
          "answer": 0,
          "explain": "Security basics cho automation engineer."
        }
      ]
    },
    "api1": {
      "title": "Fundamentals & HTTP",
      "questions": [
        {
          "q": "API là gì (interview)?",
          "options": [
            "Contract cho phép app giao tiếp qua request/response",
            "Chỉ website UI",
            "Chỉ database",
            "Chỉ JSON"
          ],
          "answer": 0,
          "explain": "API = interface giữa systems."
        },
        {
          "q": "REST stateless nghĩa?",
          "options": [
            "Mỗi request đủ context, server không nhớ session state",
            "Không HTTP",
            "Luôn cần cookie session",
            "Chỉ SOAP"
          ],
          "answer": 0,
          "explain": "Stateless = scale horizontal dễ."
        },
        {
          "q": "GET idempotent?",
          "options": [
            "Có — gọi nhiều lần không đổi resource (lý tưởng)",
            "Không",
            "Chỉ POST",
            "Luôn tạo mới"
          ],
          "answer": 0,
          "explain": "Idempotent quan trọng retry payment."
        },
        {
          "q": "POST tạo resource status thường?",
          "options": [
            "201 Created",
            "200 always",
            "404",
            "401"
          ],
          "answer": 0,
          "explain": "201 + Location header chuẩn REST."
        },
        {
          "q": "401 vs 403?",
          "options": [
            "401: chưa auth; 403: đã auth nhưng forbidden",
            "Giống nhau",
            "Ngược",
            "Không HTTP"
          ],
          "answer": 0,
          "explain": "Câu hỏi classic phỏng vấn API."
        },
        {
          "q": "404 khi nào?",
          "options": [
            "Resource/URL không tồn tại",
            "Auth fail",
            "Validation error",
            "Server crash"
          ],
          "answer": 0,
          "explain": "404 Not Found resource."
        },
        {
          "q": "400 Bad Request?",
          "options": [
            "Client gửi sai format/validation",
            "Server down",
            "Auth",
            "Success"
          ],
          "answer": 0,
          "explain": "400 = lỗi phía client payload."
        },
        {
          "q": "SOAP vs REST phỏng vấn?",
          "options": [
            "SOAP XML, contract chặt, enterprise; REST nhẹ JSON phổ biến",
            "REST dùng XML only",
            "SOAP nhanh hơn luôn",
            "Giống nhau"
          ],
          "answer": 0,
          "explain": "Biết context chọn protocol."
        },
        {
          "q": "GraphQL over-fetching giải quyết?",
          "options": [
            "Client chọn đúng fields cần",
            "Luôn lấy full table",
            "Chỉ SOAP",
            "Không query"
          ],
          "answer": 0,
          "explain": "GraphQL = flexible query, learning curve cao."
        },
        {
          "q": "Request header Authorization: Bearer?",
          "options": [
            "Gửi JWT/token",
            "Basic only",
            "Cookie only",
            "Không auth"
          ],
          "answer": 0,
          "explain": "Bearer token phổ biến REST."
        },
        {
          "q": "Response body validate ngoài status?",
          "options": [
            "Schema, business fields, DB state",
            "Chỉ status 200",
            "Chỉ time",
            "Không assert"
          ],
          "answer": 0,
          "explain": "API test 3 lớp: response, DB, side effect."
        },
        {
          "q": "Idempotency payment POST issue?",
          "options": [
            "Retry có thể double charge nếu không idempotency key",
            "Không vấn đề",
            "GET only",
            "Không test"
          ],
          "answer": 0,
          "explain": "POST không idempotent — design key quan trọng."
        },
        {
          "q": "PUT vs PATCH?",
          "options": [
            "PUT thay thế resource; PATCH partial update",
            "Giống nhau",
            "PATCH tạo mới",
            "PUT chỉ delete"
          ],
          "answer": 0,
          "explain": "PATCH cho update một phần."
        },
        {
          "q": "DELETE idempotent?",
          "options": [
            "Có — xóa lần 2 vẫn 'đã xóa' (404 hoặc 204)",
            "Không",
            "Tạo mới",
            "Chỉ POST"
          ],
          "answer": 0,
          "explain": "DELETE retry an toàn hơn POST create."
        },
        {
          "q": "DB verification sau POST user?",
          "options": [
            "SELECT confirm row exists, field đúng",
            "Chỉ trust API 201",
            "Không cần DB",
            "Chỉ UI"
          ],
          "answer": 0,
          "explain": "DB verify catch bug API 'fake success'."
        },
        {
          "q": "500 Internal Server Error?",
          "options": [
            "Lỗi server — log phía server",
            "Client typo",
            "Auth",
            "Not found"
          ],
          "answer": 0,
          "explain": "500 = triage backend/logs."
        },
        {
          "q": "Contract test benefit?",
          "options": [
            "Phát hiện breaking change API sớm",
            "Thay manual UI",
            "Không API",
            "Chỉ load"
          ],
          "answer": 0,
          "explain": "Consumer-driven contracts."
        },
        {
          "q": "Rate limit 429?",
          "options": [
            "Too Many Requests — cần backoff",
            "Auth fail",
            "OK",
            "Created"
          ],
          "answer": 0,
          "explain": "429 = throttle/quota."
        },
        {
          "q": "JSON Content-Type?",
          "options": [
            "application/json",
            "text/html",
            "multipart only",
            "soap+xml only"
          ],
          "answer": 0,
          "explain": "Header đúng cho REST JSON."
        },
        {
          "q": "Negative test SQL injection API?",
          "options": [
            "Payload malicious → không 500, reject/sanitize",
            "Chỉ happy path",
            "Không security",
            "Chỉ GET"
          ],
          "answer": 0,
          "explain": "Security negative là must-know."
        }
      ]
    },
    "api2": {
      "title": "Auth & Security",
      "questions": [
        {
          "q": "Authentication vs Authorization?",
          "options": [
            "AuthN: who are you; AuthZ: what you can do",
            "Giống nhau",
            "Ngược",
            "Không liên quan"
          ],
          "answer": 0,
          "explain": "Nhầm 401/403 thường từ nhầm hai khái niệm."
        },
        {
          "q": "Basic Auth encode?",
          "options": [
            "Base64(username:password) trong header",
            "Plain text header",
            "JWT only",
            "OAuth1 only"
          ],
          "answer": 0,
          "explain": "Basic đơn giản, HTTPS bắt buộc."
        },
        {
          "q": "JWT structure?",
          "options": [
            "header.payload.signature",
            "Chỉ JSON body",
            "SQL table",
            "Cookie only"
          ],
          "answer": 0,
          "explain": "JWT = signed claims."
        },
        {
          "q": "Bearer token gửi như?",
          "options": [
            "Authorization: Bearer <token>",
            "Body only",
            "Query only",
            "Footer HTML"
          ],
          "answer": 0,
          "explain": "Standard header format."
        },
        {
          "q": "Token expired test expect?",
          "options": [
            "401/403 + refresh flow nếu có",
            "200 OK",
            "201",
            "500 only"
          ],
          "answer": 0,
          "explain": "Negative auth critical."
        },
        {
          "q": "Role-based access test?",
          "options": [
            "User role A không gọi được API admin",
            "Chỉ login",
            "Chỉ UI",
            "Không negative"
          ],
          "answer": 0,
          "explain": "AuthZ matrix test cases."
        },
        {
          "q": "OAuth2 authorization code flow?",
          "options": [
            "Redirect login, exchange code for token",
            "Chỉ Basic",
            "Không token",
            "Chỉ SOAP"
          ],
          "answer": 0,
          "explain": "OAuth phổ biến third-party login."
        },
        {
          "q": "Session cookie vs JWT stateless?",
          "options": [
            "Session server-side state; JWT client holds",
            "Giống nhau",
            "JWT server session",
            "Cookie không HTTP"
          ],
          "answer": 0,
          "explain": "Tradeoff scale vs revoke."
        },
        {
          "q": "Brute force login API test?",
          "options": [
            "Lockout/rate limit sau N fail",
            "Unlimited try",
            "200 always",
            "Skip"
          ],
          "answer": 0,
          "explain": "Security requirement thực tế."
        },
        {
          "q": "Horizontal privilege escalation?",
          "options": [
            "User A access data user B cùng role",
            "Vertical admin",
            "SQL only",
            "UI only"
          ],
          "answer": 0,
          "explain": "IDOR hay gặp — test với 2 user."
        },
        {
          "q": "Vertical privilege?",
          "options": [
            "User thường gọi API admin",
            "Same user data",
            "GET only",
            "Cookie size"
          ],
          "answer": 0,
          "explain": "403 expected cho user thường."
        },
        {
          "q": "HTTPS why?",
          "options": [
            "Encrypt transit, protect token/password",
            "Faster",
            "Required JSON",
            "Optional always"
          ],
          "answer": 0,
          "explain": "Không test auth trên HTTP production."
        },
        {
          "q": "API key in query string risk?",
          "options": [
            "Leak log/referrer — prefer header",
            "Best practice",
            "Most secure",
            "Required"
          ],
          "answer": 0,
          "explain": "Security review hay chỉ ra."
        },
        {
          "q": "Refresh token purpose?",
          "options": [
            "Lấy access token mới không re-login",
            "Delete user",
            "Patch only",
            "DB only"
          ],
          "answer": 0,
          "explain": "Refresh flow test riêng."
        },
        {
          "q": "CORS error thường ở?",
          "options": [
            "Browser cross-origin — không phải Postman",
            "Server down",
            "DB",
            "JUnit"
          ],
          "answer": 0,
          "explain": "Postman bypass CORS — hiểu browser vs API tool."
        },
        {
          "q": "Sensitive data in response?",
          "options": [
            "Không trả password hash, full PAN",
            "Trả hết cho debug",
            "OK production",
            "Chỉ UI"
          ],
          "answer": 0,
          "explain": "Data minimization security."
        },
        {
          "q": "Multi-tenant auth test?",
          "options": [
            "Tenant A token không access tenant B data",
            "Single user",
            "No header",
            "Skip DB"
          ],
          "answer": 0,
          "explain": "SaaS critical scenario."
        },
        {
          "q": "Logout invalidate token?",
          "options": [
            "Token cũ không dùng được",
            "Token forever",
            "200 only",
            "No test"
          ],
          "answer": 0,
          "explain": "Revocation/blacklist test."
        },
        {
          "q": "MFA API flow test?",
          "options": [
            "Step password + OTP",
            "Single step only",
            "No negative",
            "UI only"
          ],
          "answer": 0,
          "explain": "Multi-step auth automation."
        },
        {
          "q": "Security header HSTS?",
          "options": [
            "Force HTTPS browser",
            "JWT sign",
            "CORS",
            "JSON schema"
          ],
          "answer": 0,
          "explain": "Ops/security awareness cho tester."
        },
        {
          "q": "Interview: auth test checklist?",
          "options": [
            "AuthN fail/success, AuthZ matrix, token lifecycle, injection",
            "Chỉ 200",
            "Chỉ UI click",
            "Không negative"
          ],
          "answer": 0,
          "explain": "Structured answer ghi điểm."
        }
      ]
    },
    "api3": {
      "title": "RestAssured Automation",
      "questions": [
        {
          "q": "RestAssured given().when().then()?",
          "options": [
            "Arrange request, act call, assert response",
            "Chỉ assert",
            "Chỉ UI",
            "Chỉ SQL"
          ],
          "answer": 0,
          "explain": "BDD style API test RA."
        },
        {
          "q": "given().baseUri() set?",
          "options": [
            "Base URL API",
            "Database",
            "Browser",
            "TestNG xml only"
          ],
          "answer": 0,
          "explain": "baseUri + path = full URL."
        },
        {
          "q": ".statusCode(200) trong then()?",
          "options": [
            "Assert HTTP status",
            "Assert body only",
            "Header only",
            "Time only"
          ],
          "answer": 0,
          "explain": "Status assert cơ bản."
        },
        {
          "q": ".body(\"name\", equalTo(\"x\"))?",
          "options": [
            "JsonPath assert field",
            "XPath UI",
            "SQL",
            "CSS"
          ],
          "answer": 0,
          "explain": "Hamcrest matchers trong RA."
        },
        {
          "q": "POST with body JSON?",
          "options": [
            "given().contentType(JSON).body(obj).when().post()",
            "Chỉ GET",
            "Chỉ delete",
            "Không body"
          ],
          "answer": 0,
          "explain": "Serialization object/map to JSON."
        },
        {
          "q": "extract().path(\"id\") dùng?",
          "options": [
            "Lấy value chain request sau",
            "Screenshot",
            "Driver quit",
            "Compile"
          ],
          "answer": 0,
          "explain": "Chaining create → get by id."
        },
        {
          "q": "RequestSpec reuse?",
          "options": [
            "given(requestSpec) DRY headers/auth",
            "Copy paste mọi test",
            "Không RA",
            "UI POM only"
          ],
          "answer": 0,
          "explain": "Spec builder pattern RA."
        },
        {
          "q": "ResponseSpec validate chung?",
          "options": [
            "expect status, contentType chung mọi test",
            "Mỗi test khác hẳn",
            "Không assert",
            "Manual only"
          ],
          "answer": 0,
          "explain": "ResponseSpec = shared assertions."
        },
        {
          "q": "log().all() khi debug?",
          "options": [
            "In request/response detail",
            "Production always",
            "Thay assert",
            "Delete test"
          ],
          "answer": 0,
          "explain": "Log verbose khi triage fail."
        },
        {
          "q": "TestNG @BeforeClass API setup?",
          "options": [
            "Base URI, auth token once per class",
            "Mỗi assert",
            "Không setup",
            "UI only"
          ],
          "answer": 0,
          "explain": "Fixture pattern RA + TestNG."
        },
        {
          "q": "DataProvider + RestAssured?",
          "options": [
            "Nhiều row data gọi cùng test logic",
            "Không data-driven",
            "Chỉ manual",
            "Chỉ CSV UI"
          ],
          "answer": 0,
          "explain": "Combine TestNG data + RA."
        },
        {
          "q": "API Page Object?",
          "options": [
            "Class UsersApi với methods getUser(), createUser()",
            "Locator By.id",
            "Driver only",
            "Không POM"
          ],
          "answer": 0,
          "explain": "POM concept áp API layer."
        },
        {
          "q": "BaseTest chứa spec/auth?",
          "options": [
            "requestSpec, token refresh helper",
            "Tất cả test logic",
            "Production app code",
            "Không nên"
          ],
          "answer": 0,
          "explain": "BaseTest infrastructure RA."
        },
        {
          "q": "Schema validation RA?",
          "options": [
            "body(matchesJsonSchemaInClasspath)",
            "Chỉ status",
            "Chỉ UI",
            "Không JSON"
          ],
          "answer": 0,
          "explain": "Contract schema validation."
        },
        {
          "q": "Query param given().queryParam()?",
          "options": [
            "Thêm ?key=value URL",
            "Body only",
            "Header only",
            "Cookie only"
          ],
          "answer": 0,
          "explain": "Query vs path vs body params."
        },
        {
          "q": "Path param get(\"/users/{id}\", id)?",
          "options": [
            "URL template variable",
            "Query only",
            "Header only",
            "SOAP only"
          ],
          "answer": 0,
          "explain": "Path param RESTful resource id."
        },
        {
          "q": "Authentication RA preemptive Basic?",
          "options": [
            "given().auth().preemptive().basic(user, pass)",
            "Không auth RA",
            "UI login only",
            "Manual only"
          ],
          "answer": 0,
          "explain": "RA hỗ trợ auth helpers."
        },
        {
          "q": "Parallel TestNG + RA lưu ý?",
          "options": [
            "Test independent, không share mutable state",
            "Shared static token unsafe",
            "One thread only",
            "No data"
          ],
          "answer": 0,
          "explain": "Thread safety khi parallel API tests."
        },
        {
          "q": "Allure + RestAssured?",
          "options": [
            "Attach request/response vào report",
            "Thay TestNG",
            "Thay RA",
            "Không report"
          ],
          "answer": 0,
          "explain": "Reporting stakeholder-friendly."
        },
        {
          "q": "Interview: RA vs Postman?",
          "options": [
            "RA = code, CI, version control; Postman = explore/manual",
            "Giống hẳn",
            "Postman CI better always",
            "RA không code"
          ],
          "answer": 0,
          "explain": "Biết khi nào tool nào — senior answer."
        }
      ]
    }
  }
};
