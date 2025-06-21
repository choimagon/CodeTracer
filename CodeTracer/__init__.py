import sys
import threading
import os 

class CT:
    def __init__(self):
        self._original_trace = None
        self.logs = []

        # ANSI 색상
        self.COLOR_FUNC = '\033[96m'   # 하늘색
        self.COLOR_CLASS = '\033[92m'  # 연두색
        self.COLOR_RESET = '\033[0m'

    def _trace_func(self, frame, event, arg):
        # CodeTracer 내부 함수는 제외 (main 스크립트에서 실행된 코드만 추적)
        if frame.f_globals.get("__name__") != "__main__":
            return

        if event == 'call':
            code = frame.f_code
            func_name = code.co_name
            filename = code.co_filename
            lineno = frame.f_lineno

            if 'self' in frame.f_locals:
                cls_name = type(frame.f_locals['self']).__name__
                log = f"{self.COLOR_CLASS}[CLASS:{cls_name}.{func_name}] → {filename}:{lineno}{self.COLOR_RESET}"
            else:
                log = f"{self.COLOR_FUNC}[FUNC:{func_name}] → {filename}:{lineno}{self.COLOR_RESET}"
            
            self.logs.append(log)

        return self._trace_func

    def start(self):
        self._original_trace = sys.gettrace()
        sys.settrace(self._trace_func)
        threading.settrace(self._trace_func)

    def stop(self):
        sys.settrace(self._original_trace)
        threading.settrace(None)
        print("\n\n\n")
        line = "=" * 20
        print(line)
        print("\n⬜ 코드 실행 추적 결과:\n")
        for log in self.logs:
            print(log)
        print("\n" + line)

    def filelist(self, path=None, prefix="", show_header=True):
        if path is None:
            path = os.path.dirname(os.path.abspath(__file__))
        if show_header:
            print("\n📂 파일 구조:")
        entries = sorted(os.listdir(path))
        entries = [e for e in entries if not e.startswith('.')]  # 숨김 파일 제외

        for i, entry in enumerate(entries):
            full_path = os.path.join(path, entry)
            connector = "└── " if i == len(entries) - 1 else "├── "
            print(prefix + connector + entry)
            if os.path.isdir(full_path):
                extension = "    " if i == len(entries) - 1 else "│   "
                self.filelist(full_path, prefix + extension, show_header=False)
