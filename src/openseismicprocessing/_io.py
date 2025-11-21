import segyio
import pandas as pd
import re

def open_segy_data(filePath, ignore_geometry = True):
    return segyio.open(filePath, "r", ignore_geometry=ignore_geometry)

def parse_trace_headers(segyfile):
    '''
    Parse the segy file trace headers into a pandas dataframe.
    Column names are defined from segyio internal tracefield
    One row per trace
    '''
    # Get all header keys
    n_traces = segyfile.tracecount
    headers = segyio.tracefield.keys
    # Initialize dataframe with trace id as index and headers as columns
    df = pd.DataFrame(index=range(0, n_traces),
                      columns=headers.keys())
    # Fill dataframe with all header values
    for k, v in headers.items():
        df[k] = segyfile.attributes(v)[:]
    return df

def parse_text_header(segyfile):
    """
    Format SEGY text header into a clean, readable dictionary.
    """
    try:
        raw_header = segyio.tools.wrap(segyfile.text[0])
    except Exception as e:
        print(f"❌ Error wrapping text header: {e}")
        return None

    lines = raw_header.splitlines()
    if not lines:
        print("❌ Error: Unexpected header format.")
        return None

    cleaned = []
    for line in lines:
        # Remove leading Cxx markers if present
        m = re.match(r"\\s*C\\s*\\d{2}\\s*(.*)", line)
        cleaned.append((m.group(1) if m else line).strip())

    clean_header = {f"C{str(i).rjust(2, '0')}": text for i, text in enumerate(cleaned, start=1)}
    return clean_header
